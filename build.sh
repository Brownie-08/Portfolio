#!/bin/bash
set -e

echo "🔧 Starting build process..."

echo "📦 Upgrading pip..."
python -m pip install --upgrade pip

echo "📋 Installing requirements..."
python -m pip install -r requirements.txt

echo "🎨 Compiling SCSS files..."
# Try to compress, but don't fail if it doesn't work
if python manage.py compress --force 2>/dev/null; then
    echo "✅ SCSS compilation successful"
else
    echo "⚠️  SCSS compilation failed, but continuing..."
fi

echo "🎨 Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "✅ Build completed successfully!"
