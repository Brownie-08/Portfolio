#!/usr/bin/env bash
set -o errexit

echo "Starting build process..."

echo "Upgrading pip..."
pip install --upgrade pip

echo "Installing Python requirements..."
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --noinput --settings=portfolio_project.settings.production

echo "Running database migrations..."
python manage.py migrate --noinput --settings=portfolio_project.settings.production

echo "Build completed successfully!"
