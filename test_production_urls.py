#!/usr/bin/env python
"""
Quick script to test image URLs with production settings
"""
import os
import django

# Force production settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_project.settings.railway')
django.setup()

from django.conf import settings
from portfolio.models import Project, PersonalInfo, Testimonial

def test_production_urls():
    print("=== RAILWAY PRODUCTION URL TEST ===\n")
    
    print("1. SETTINGS CHECK:")
    print(f"   DEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}")
    print(f"   MEDIA_URL: '{settings.MEDIA_URL}'")
    print(f"   MEDIA_ROOT: '{getattr(settings, 'MEDIA_ROOT', 'NOT SET')}'")
    
    print(f"\n2. CLOUDINARY CONFIG:")
    try:
        import cloudinary
        config = cloudinary.config()
        print(f"   Cloud Name: {config.cloud_name}")
        print(f"   Secure: {config.secure}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print(f"\n3. IMAGE URL TESTS:")
    
    # Test Project Images
    projects = Project.objects.filter(image__isnull=False)[:3]
    for project in projects:
        try:
            url = project.image.url
            print(f"   ✅ {project.title[:30]:<30}: {url}")
            
            # Verify it's a proper Cloudinary URL
            if url.startswith('https://res.cloudinary.com/'):
                print(f"      Type: Cloudinary HTTPS ✅")
            elif url.startswith('/media/'):
                print(f"      Type: LOCAL PATH ❌ (BROKEN IN RAILWAY)")
            else:
                print(f"      Type: UNKNOWN ⚠️")
                
        except Exception as e:
            print(f"   ❌ {project.title[:30]:<30}: ERROR - {e}")
    
    # Test Profile Image
    try:
        personal_info = PersonalInfo.objects.first()
        if personal_info and personal_info.profile_image:
            url = personal_info.profile_image.url
            print(f"   ✅ Profile Image               : {url}")
            
            if url.startswith('https://res.cloudinary.com/'):
                print(f"      Type: Cloudinary HTTPS ✅")
            else:
                print(f"      Type: NOT CLOUDINARY ❌")
                
    except Exception as e:
        print(f"   ❌ Profile Image               : ERROR - {e}")
    
    print(f"\n4. VERDICT:")
    print("   If all URLs start with 'https://res.cloudinary.com/' - ✅ READY FOR RAILWAY")
    print("   If any URLs start with '/media/' - ❌ STILL BROKEN IN RAILWAY")
    print("   Make sure to redeploy to Railway after this fix!")

if __name__ == '__main__':
    test_production_urls()
