#!/bin/bash
set -e

echo "🔧 Starting build process..."

echo "📦 Upgrading pip..."
python -m pip install --upgrade pip

echo "📋 Installing requirements..."
python -m pip install -r requirements.txt

echo "🎨 Collecting static files..."
python manage.py collectstatic --noinput

echo "✅ Build completed successfully!"
