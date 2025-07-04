#!/bin/bash
set -e

echo "🚀 Starting Django application..."

# Set default port if not provided
export PORT=${PORT:-8000}

echo "📦 Port: $PORT"
echo "🔧 Django Settings: $DJANGO_SETTINGS_MODULE"

# Run database migrations
echo "🗄️ Running database migrations..."
python manage.py migrate --noinput

# Check Django configuration
echo "🔍 Checking Django configuration..."
python manage.py check --deploy

# Test database connection
echo "🔗 Testing database connection..."
python manage.py shell -c "from django.db import connection; connection.ensure_connection(); print('✅ Database connected successfully')"

# Start gunicorn
echo "🚀 Starting gunicorn server on 0.0.0.0:$PORT..."
exec gunicorn portfolio_project.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --worker-class sync \
    --worker-connections 1000 \
    --timeout 120 \
    --keepalive 5 \
    --max-requests 1000 \
    --max-requests-jitter 100 \
    --access-logfile - \
    --error-logfile - \
    --log-level info
