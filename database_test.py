#!/usr/bin/env python
"""
Simple database configuration test script for Railway deployment.
Run this to verify DATABASE_URL is working correctly.
"""

import os
import sys
import django
from pathlib import Path

# Add the project root to Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# Set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_project.settings.railway')
django.setup()

from django.conf import settings
from django.db import connection

def test_database():
    """Test database connection and configuration."""
    print("🔧 Testing Database Configuration")
    print("-" * 50)
    
    # Check DATABASE_URL environment variable
    database_url = os.environ.get('DATABASE_URL')
    print(f"📊 DATABASE_URL: {'✅ Present' if database_url else '❌ Missing'}")
    if database_url:
        if 'postgresql' in database_url.lower():
            print(f"   Database Type: PostgreSQL")
        elif 'sqlite' in database_url.lower():
            print(f"   Database Type: SQLite")
        else:
            print(f"   Database Type: Other ({database_url[:20]}...)")
    
    # Check Django DATABASES config
    db_config = settings.DATABASES['default']
    print(f"🗄️  Django Database Engine: {db_config.get('ENGINE', 'Not configured')}")
    print(f"📍 Database Name: {db_config.get('NAME', 'Not configured')}")
    
    # Test actual connection
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            print(f"✅ Database Connection: Success (result: {result[0]})")
    except Exception as e:
        print(f"❌ Database Connection: Failed - {e}")
        return False
    
    print("-" * 50)
    print("🎉 Database configuration test completed!")
    return True

if __name__ == "__main__":
    success = test_database()
    sys.exit(0 if success else 1)
