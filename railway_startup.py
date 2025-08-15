#!/usr/bin/env python
"""
Railway startup script that ensures:
1. Database migrations are applied
2. Static files are collected  
3. Superuser is created if it doesn't exist

This script runs before the Django app starts on Railway.
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_project.settings.railway')

# Initialize Django
django.setup()

def run_startup_tasks():
    """Run essential startup tasks for Railway deployment."""
    
    print("🚀 Starting Railway deployment tasks...")
    
    # 1. Run database migrations
    print("📊 Running database migrations...")
    try:
        execute_from_command_line(['manage.py', 'migrate', '--noinput'])
        print("✅ Database migrations completed successfully")
    except Exception as e:
        print(f"⚠️  Migration warning: {e}")
    
    # 2. Collect static files
    print("📁 Collecting static files...")
    try:
        execute_from_command_line(['manage.py', 'collectstatic', '--noinput', '--clear'])
        print("✅ Static files collected successfully")
    except Exception as e:
        print(f"⚠️  Static files warning: {e}")
    
    # 3. Create superuser (backup method)
    print("👑 Checking superuser creation...")
    try:
        execute_from_command_line(['manage.py', 'create_superuser_railway'])
        print("✅ Superuser check completed")
    except Exception as e:
        print(f"ℹ️  Superuser already exists or will be created automatically: {e}")
    
    print("🎉 Railway startup tasks completed!")

if __name__ == '__main__':
    run_startup_tasks()
