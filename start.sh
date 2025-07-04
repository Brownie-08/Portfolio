#!/bin/bash
set -e

echo "🚀 Starting Django Portfolio Application..."
echo "📍 Working Directory: $(pwd)"
echo "🐍 Python Version: $(python --version)"

# Set default port if not provided
export PORT=${PORT:-8000}
export DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE:-portfolio_project.settings.production}

echo "📦 Port: $PORT"
echo "🔧 Django Settings: $DJANGO_SETTINGS_MODULE"
echo "🗃️ Database URL: ${DATABASE_URL:0:20}..."

# Basic Django check (without deploy flags that might fail)
echo "🔍 Checking Django basic configuration..."
python manage.py check

# Wait for database to be ready (Railway MySQL might take a moment)
echo "⏳ Waiting for database to be ready..."
for i in {1..30}; do
    if python manage.py shell -c "from django.db import connection; connection.ensure_connection(); print('✅ Database connected')" 2>/dev/null; then
        echo "✅ Database connection successful!"
        break
    else
        echo "⏳ Database not ready yet, waiting... ($i/30)"
        sleep 2
    fi
    if [ $i -eq 30 ]; then
        echo "❌ Database connection failed after 60 seconds"
        echo "🔍 Attempting to show database error:"
        python manage.py shell -c "from django.db import connection; connection.ensure_connection()"
        exit 1
    fi
done

# Run database migrations
echo "🗄️ Running database migrations..."
python manage.py migrate --noinput

# Create superuser if needed (non-interactive)
echo "👤 Checking for superuser..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('✅ Superuser created: admin/admin123')
else:
    print('✅ Superuser already exists')
" || echo "⚠️ Superuser creation skipped"

# Test health endpoint
echo "🔍 Testing health endpoints..."
python manage.py shell -c "
from django.test import Client
c = Client()
try:
    response = c.get('/health/')
    print(f'✅ Health check: {response.status_code}')
except Exception as e:
    print(f'⚠️ Health check failed: {e}')
" || echo "⚠️ Health check test skipped"

echo "🚀 Starting gunicorn server on 0.0.0.0:$PORT..."
echo "🌐 Application will be available at: http://0.0.0.0:$PORT"

# Start gunicorn with Railway-optimized settings
exec gunicorn portfolio_project.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 1 \
    --worker-class sync \
    --worker-connections 1000 \
    --timeout 300 \
    --keepalive 5 \
    --max-requests 1000 \
    --max-requests-jitter 100 \
    --preload \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    --capture-output
