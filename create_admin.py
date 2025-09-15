#!/usr/bin/env python
"""
Create admin user for production deployment.
This script creates a superuser if one doesn't exist.
"""

import os
import sys
import django
from pathlib import Path

# Add the project root to Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# Set up Django settings - use environment variable or default to render
settings_module = os.environ.get('DJANGO_SETTINGS_MODULE', 'portfolio_project.settings.render')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

try:
    django.setup()
    
    from django.contrib.auth.models import User
    from django.core.management import execute_from_command_line
    
    def create_admin_user():
        """Create admin user if it doesn't exist."""
        
        # Get admin credentials from environment variables
        admin_username = os.environ.get('ADMIN_USERNAME', 'admin')
        admin_email = os.environ.get('ADMIN_EMAIL', 'admin@example.com')
        admin_password = os.environ.get('ADMIN_PASSWORD', 'changeme123!')
        
        print(f"🔧 Checking for admin user: {admin_username}")
        
        try:
            # Check if admin user already exists
            if User.objects.filter(username=admin_username).exists():
                print(f"✅ Admin user '{admin_username}' already exists.")
                return True
                
            # Create admin user
            admin_user = User.objects.create_superuser(
                username=admin_username,
                email=admin_email,
                password=admin_password
            )
            
            print(f"✅ Created admin user successfully!")
            print(f"   Username: {admin_username}")
            print(f"   Email: {admin_email}")
            print(f"   Admin URL: /admin/")
            print(f"🔒 Password: {admin_password}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error creating admin user: {e}")
            return False
    
    if __name__ == "__main__":
        success = create_admin_user()
        sys.exit(0 if success else 1)
        
except Exception as e:
    print(f"❌ Error setting up Django: {e}")
    print("This script should be run after Django is properly configured.")
    sys.exit(1)