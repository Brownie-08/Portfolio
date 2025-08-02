#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput --clear

# Run migrations
python manage.py migrate --noinput

# Create staticfiles_build directory for Vercel
mkdir -p staticfiles_build
cp -r static staticfiles_build/
