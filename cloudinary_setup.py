#!/usr/bin/env python
"""
Setup script to configure Cloudinary for production media storage
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_project.settings.dev')
django.setup()

def setup_cloudinary():
    print("=== CLOUDINARY SETUP FOR PRODUCTION ===")
    print()
    print("Your portfolio is deployed on Render, which doesn't provide persistent file storage.")
    print("This means uploaded images get deleted every time the app redeploys.")
    print()
    print("SOLUTION: Use Cloudinary (free tier) for image storage")
    print()
    print("Steps to fix this:")
    print("1. Sign up for Cloudinary (free): https://cloudinary.com/users/register/free")
    print("2. Get your credentials from the dashboard")
    print("3. Add environment variables to Render")
    print("4. Update requirements.txt")
    print("5. Redeploy")
    print()
    print("After completing these steps, your images will be stored on Cloudinary")
    print("and will persist through deployments!")

if __name__ == '__main__':
    setup_cloudinary()
