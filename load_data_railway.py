#!/usr/bin/env python
"""
Script to load fixture data into Railway production database.
Run this after deployment to restore development data.
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

from django.core.management import execute_from_command_line

def load_fixture_data():
    """Load the exported fixture data into the database."""
    print("🔄 Loading fixture data into Railway database...")
    
    # Check if data.json exists
    data_file = BASE_DIR / 'data.json'
    if not data_file.exists():
        print("❌ Error: data.json not found. Please run the data export first.")
        return False
    
    try:
        # Load the fixture data
        execute_from_command_line(['manage.py', 'loaddata', 'data.json'])
        print("✅ Successfully loaded fixture data!")
        return True
        
    except Exception as e:
        print(f"❌ Error loading fixture data: {e}")
        return False

if __name__ == "__main__":
    success = load_fixture_data()
    sys.exit(0 if success else 1)
