#!/usr/bin/env python
"""
Railway Production Image Diagnosis Script
Run this in Railway terminal to diagnose image upload issues
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_project.settings.railway')
django.setup()

from django.conf import settings
from portfolio.models import Project, PersonalInfo, Testimonial

def diagnose_railway_images():
    print("=== RAILWAY PRODUCTION IMAGE DIAGNOSIS ===\n")
    
    print("1. ENVIRONMENT VARIABLES:")
    env_vars = [
        'USE_CLOUDINARY',
        'USE_LOCAL_STORAGE',
        'CLOUDINARY_CLOUD_NAME',
        'CLOUDINARY_API_KEY',
        'CLOUDINARY_API_SECRET',
        'DJANGO_SETTINGS_MODULE'
    ]
    
    for var in env_vars:
        value = os.environ.get(var, 'NOT SET')
        if 'SECRET' in var or 'KEY' in var:
            display_value = value[:8] + '***' if value != 'NOT SET' and len(value) > 8 else value
        else:
            display_value = value
        print(f"   {var}: {display_value}")
    
    print(f"\n2. DJANGO STORAGE CONFIGURATION:")
    print(f"   DEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}")
    print(f"   MEDIA_URL: {settings.MEDIA_URL}")
    print(f"   MEDIA_ROOT: {getattr(settings, 'MEDIA_ROOT', 'NOT SET')}")
    
    print(f"\n3. CLOUDINARY CONNECTION TEST:")
    try:
        if 'cloudinary' in settings.DEFAULT_FILE_STORAGE.lower():
            import cloudinary
            import cloudinary.api
            result = cloudinary.api.ping()
            print(f"   ✅ Cloudinary connected: {result.get('status', 'unknown')}")
            
            # Get Cloudinary config
            config = cloudinary.config()
            print(f"   Cloud Name: {config.cloud_name}")
            print(f"   API Key: {config.api_key}")
            print(f"   Secure: {config.secure}")
        else:
            print("   ⚠️ Not using Cloudinary storage")
    except Exception as e:
        print(f"   ❌ Cloudinary error: {e}")
    
    print(f"\n4. DATABASE IMAGE PATHS:")
    # Check projects
    projects = Project.objects.all()[:3]
    print(f"   Projects ({projects.count()}):")
    for project in projects:
        if project.image:
            print(f"   - {project.title}: {project.image.name}")
            try:
                url = project.image.url
                print(f"     URL: {url}")
                # Check if URL is accessible
                if 'cloudinary.com' in url:
                    print(f"     Type: Cloudinary URL ✅")
                else:
                    print(f"     Type: Local URL - May not work in Railway")
            except Exception as e:
                print(f"     URL ERROR: {e}")
        else:
            print(f"   - {project.title}: NO IMAGE")
    
    # Check personal info
    try:
        personal_info = PersonalInfo.objects.first()
        if personal_info and personal_info.profile_image:
            print(f"\n   Profile Image:")
            print(f"   - Path: {personal_info.profile_image.name}")
            try:
                url = personal_info.profile_image.url
                print(f"   - URL: {url}")
                if 'cloudinary.com' in url:
                    print(f"   - Type: Cloudinary URL ✅")
                else:
                    print(f"   - Type: Local URL - May not work in Railway")
            except Exception as e:
                print(f"   - URL ERROR: {e}")
        else:
            print(f"\n   Profile Image: NOT SET")
    except Exception as e:
        print(f"\n   Profile Image ERROR: {e}")
    
    print(f"\n5. RECOMMENDED FIXES:")
    
    # Check if environment variables are correct
    use_cloudinary = os.environ.get('USE_CLOUDINARY', 'False').lower() in ('true', '1', 't')
    use_local_storage = os.environ.get('USE_LOCAL_STORAGE', 'True').lower() in ('true', '1', 't')
    
    if not use_cloudinary:
        print("   ❌ SET: USE_CLOUDINARY=True in Railway environment variables")
    
    if use_local_storage:
        print("   ❌ SET: USE_LOCAL_STORAGE=False in Railway environment variables")
    
    if not os.environ.get('CLOUDINARY_CLOUD_NAME'):
        print("   ❌ SET: CLOUDINARY_CLOUD_NAME in Railway environment variables")
    
    if not os.environ.get('CLOUDINARY_API_KEY'):
        print("   ❌ SET: CLOUDINARY_API_KEY in Railway environment variables")
    
    if not os.environ.get('CLOUDINARY_API_SECRET'):
        print("   ❌ SET: CLOUDINARY_API_SECRET in Railway environment variables")
    
    if use_cloudinary and not use_local_storage:
        print("   ✅ Environment variables look correct for Cloudinary")
        print("   📝 Try uploading a NEW image through admin dashboard")
        print("   📝 Old images with local paths may still be broken")

if __name__ == '__main__':
    diagnose_railway_images()
