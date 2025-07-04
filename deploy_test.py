#!/usr/bin/env python
"""
Pre-deployment test script for Django portfolio.
This script simulates the production deployment process locally.
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Run a command and print its status"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(f"Output: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        print(f"Error: {e.stderr}")
        return False

def main():
    print("🚀 Django Portfolio Deployment Test")
    print("=" * 50)
    
    # Check if manage.py exists
    if not Path("manage.py").exists():
        print("❌ manage.py not found. Please run this script from the project root.")
        sys.exit(1)
    
    # Set environment variables for testing
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_project.settings.production')
    os.environ.setdefault('DEBUG', 'False')
    os.environ.setdefault('SECRET_KEY', 'test-secret-key-for-deployment-testing')
    os.environ.setdefault('COMPRESS_ENABLED', 'True')
    os.environ.setdefault('COMPRESS_OFFLINE', 'True')
    
    # Use SQLite for local testing (will be PostgreSQL in production)
    if not os.environ.get('DATABASE_URL'):
        print("INFO: Using SQLite for local testing (PostgreSQL will be used in production)")
    
    # Test steps - skip psycopg2 installation on Windows for local testing
    print("\nNote: Skipping PostgreSQL binary installation for local testing.")
    print("PostgreSQL support will be available in production deployment.\n")
    
    steps = [
        ("python manage.py check --deploy", "Running deployment checks"),
        ("python manage.py makemigrations", "Creating migrations"),
        ("python manage.py migrate", "Applying database migrations"),
        ("python manage.py collectstatic --noinput", "Collecting static files"),
        ("python manage.py compress --force", "Compressing static files"),
        ("python manage.py setup_production_data", "Setting up production data"),
    ]
    
    failed_steps = []
    
    for command, description in steps:
        if not run_command(command, description):
            failed_steps.append(description)
    
    print("\n" + "=" * 50)
    print("📊 DEPLOYMENT TEST SUMMARY")
    print("=" * 50)
    
    if failed_steps:
        print("❌ Some steps failed:")
        for step in failed_steps:
            print(f"   - {step}")
        print("\n🔧 Please fix the issues above before deploying.")
        sys.exit(1)
    else:
        print("✅ All deployment steps completed successfully!")
        print("\n🎉 Your portfolio is ready for production deployment!")
        print("\nNext steps:")
        print("1. Create a PostgreSQL database on Render")
        print("2. Set the DATABASE_URL environment variable")
        print("3. Deploy using the render.yaml configuration")
        print("4. Verify your live site is working correctly")
        
        # Test local server
        print("\n🌐 Testing local server...")
        print("Starting development server to verify setup...")
        print("Visit http://127.0.0.1:8000 to preview your portfolio")
        print("Press Ctrl+C to stop the server when you're done testing")
        
        try:
            subprocess.run(["python", "manage.py", "runserver"], check=True)
        except KeyboardInterrupt:
            print("\n👋 Server stopped. Good luck with your deployment!")
        except subprocess.CalledProcessError as e:
            print(f"\n❌ Server failed to start: {e}")

if __name__ == "__main__":
    main()
