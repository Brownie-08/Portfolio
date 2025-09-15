#!/usr/bin/env bash
# exit on error
set -o errexit

echo "🔧 Starting build process for Render deployment..."

# Update pip to latest version
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install Python dependencies
echo "📚 Installing Python requirements..."
pip install -r requirements.txt

echo "🎨 Collecting static files..."
python manage.py collectstatic --noinput --settings=portfolio_project.settings.render

echo "🗃️ Running database migrations..."
python manage.py migrate --noinput --settings=portfolio_project.settings.render

echo "👤 Creating admin user..."
python create_admin.py

echo "✅ Build completed successfully!"
