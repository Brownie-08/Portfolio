#!/usr/bin/env python
"""
Display admin credentials for Django portfolio access.
Run this to get current admin login information.
"""

import os
import sys
import django
from pathlib import Path

# Add the project root to Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# Set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_project.settings.local')
django.setup()

from django.contrib.auth.models import User

def show_admin_credentials():
    """Display current admin user credentials."""
    print("=" * 60)
    print("🔐 DJANGO ADMIN CREDENTIALS")
    print("=" * 60)
    
    try:
        # Get all superusers
        superusers = User.objects.filter(is_superuser=True)
        
        if not superusers.exists():
            print("❌ No admin users found!")
            print("\n💡 Create one with:")
            print("   python manage.py createsuperuser")
            return
        
        print(f"📊 Found {superusers.count()} admin user(s):")
        print()
        
        for i, user in enumerate(superusers, 1):
            print(f"👤 Admin User #{i}:")
            print(f"   Username: {user.username}")
            print(f"   Email: {user.email}")
            print(f"   Active: {'Yes' if user.is_active else 'No'}")
            print(f"   Staff: {'Yes' if user.is_staff else 'No'}")
            print(f"   Superuser: {'Yes' if user.is_superuser else 'No'}")
            print(f"   Last Login: {user.last_login or 'Never'}")
            print(f"   Date Joined: {user.date_joined}")
            print()
        
        print("=" * 60)
        print("🌐 ADMIN PANEL ACCESS")
        print("=" * 60)
        print("Local Development:")
        print("   URL: http://127.0.0.1:8000/admin/")
        print("   URL: http://localhost:8000/admin/")
        print()
        print("Railway Production:")
        print("   URL: https://your-railway-domain.up.railway.app/admin/")
        print()
        print("📝 Note: Use the username above with the password you set")
        print("    when creating the admin user.")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Error retrieving admin users: {e}")

if __name__ == "__main__":
    show_admin_credentials()
