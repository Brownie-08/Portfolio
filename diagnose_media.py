#!/usr/bin/env python
"""
Media Files Diagnostic Script
============================

This script helps diagnose media file serving issues in production.
Run this script to check your media configuration and Cloudinary setup.
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_project.settings.production')
django.setup()

from django.conf import settings
from portfolio.models import Project, PersonalInfo, BlogPost, Testimonial, Certification, Award

def check_django_settings():
    """Check Django media and static file settings"""
    print("=" * 50)
    print("DJANGO SETTINGS CHECK")
    print("=" * 50)
    
    print(f"DEBUG: {getattr(settings, 'DEBUG', 'Not set')}")
    print(f"MEDIA_URL: {getattr(settings, 'MEDIA_URL', 'Not set')}")
    print(f"MEDIA_ROOT: {getattr(settings, 'MEDIA_ROOT', 'Not set')}")
    print(f"STATIC_URL: {getattr(settings, 'STATIC_URL', 'Not set')}")
    print(f"STATIC_ROOT: {getattr(settings, 'STATIC_ROOT', 'Not set')}")
    print(f"USE_CLOUDINARY: {getattr(settings, 'USE_CLOUDINARY', 'Not set')}")
    print(f"USE_S3: {getattr(settings, 'USE_S3', 'Not set')}")
    
    if hasattr(settings, 'DEFAULT_FILE_STORAGE'):
        print(f"DEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}")
    
    print()

def check_cloudinary_config():
    """Check Cloudinary configuration"""
    print("=" * 50)
    print("CLOUDINARY CONFIGURATION CHECK")
    print("=" * 50)
    
    try:
        import cloudinary
        config = cloudinary.config()
        print(f"Cloudinary Cloud Name: {'Set' if config.cloud_name else 'NOT SET'}")
        print(f"Cloudinary API Key: {'Set' if config.api_key else 'NOT SET'}")
        print(f"Cloudinary API Secret: {'Set' if config.api_secret else 'NOT SET'}")
        print(f"Cloudinary Secure: {config.secure}")
        
        if hasattr(settings, 'CLOUDINARY_STORAGE'):
            print("CLOUDINARY_STORAGE settings found")
        else:
            print("WARNING: CLOUDINARY_STORAGE not configured")
            
    except ImportError:
        print("ERROR: Cloudinary not installed")
    except Exception as e:
        print(f"ERROR: Cloudinary configuration error: {e}")
    
    print()

def check_media_files():
    """Check if media files exist locally"""
    print("=" * 50)
    print("LOCAL MEDIA FILES CHECK")
    print("=" * 50)
    
    media_root = getattr(settings, 'MEDIA_ROOT', None)
    if media_root and os.path.exists(media_root):
        print(f"Media root exists: {media_root}")
        
        # Check subdirectories
        subdirs = ['images', 'images/projects', 'images/profile', 'images/blog', 'images/testimonials', 'files']
        for subdir in subdirs:
            path = os.path.join(media_root, subdir)
            if os.path.exists(path):
                count = len([f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))])
                print(f"  {subdir}: {count} files")
            else:
                print(f"  {subdir}: Directory not found")
    else:
        print(f"Media root not found: {media_root}")
    
    print()

def check_model_images():
    """Check model instances with images"""
    print("=" * 50)
    print("MODEL IMAGES CHECK")
    print("=" * 50)
    
    # Check Projects
    projects = Project.objects.filter(image__isnull=False)
    print(f"Projects with images: {projects.count()}")
    for project in projects[:5]:  # Show first 5
        try:
            url = project.image.url
            print(f"  {project.title}: {url}")
        except Exception as e:
            print(f"  {project.title}: ERROR - {e}")
    
    # Check Personal Info
    try:
        personal_info = PersonalInfo.get_active()
        if personal_info and personal_info.profile_image:
            try:
                url = personal_info.profile_image.url
                print(f"Profile image: {url}")
            except Exception as e:
                print(f"Profile image: ERROR - {e}")
        else:
            print("No profile image set")
    except Exception as e:
        print(f"Personal info error: {e}")
    
    # Check Blog Posts
    blog_posts = BlogPost.objects.filter(featured_image__isnull=False)
    print(f"Blog posts with images: {blog_posts.count()}")
    
    # Check Testimonials
    testimonials = Testimonial.objects.filter(avatar__isnull=False)
    print(f"Testimonials with avatars: {testimonials.count()}")
    
    print()

def test_cloudinary_upload():
    """Test Cloudinary upload functionality"""
    print("=" * 50)
    print("CLOUDINARY UPLOAD TEST")
    print("=" * 50)
    
    try:
        import cloudinary.uploader
        
        # Create a test image
        from PIL import Image
        import io
        
        # Create a simple test image
        img = Image.new('RGB', (100, 100), color='red')
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        # Upload to Cloudinary
        result = cloudinary.uploader.upload(
            buffer.getvalue(),
            resource_type="image",
            public_id="test_upload_diagnostic",
            overwrite=True
        )
        
        print(f"Test upload successful: {result.get('secure_url')}")
        
        # Clean up test image
        cloudinary.uploader.destroy("test_upload_diagnostic")
        print("Test image cleaned up")
        
        return True
        
    except ImportError:
        print("ERROR: Required packages not installed (cloudinary, PIL)")
        return False
    except Exception as e:
        print(f"ERROR: Upload test failed: {e}")
        return False

def suggest_fixes():
    """Suggest fixes based on the diagnosis"""
    print("=" * 50)
    print("SUGGESTED FIXES")
    print("=" * 50)
    
    fixes = []
    
    # Check if Cloudinary is properly configured
    use_cloudinary = getattr(settings, 'USE_CLOUDINARY', False)
    if use_cloudinary:
        try:
            import cloudinary
            config = cloudinary.config()
            if not all([config.cloud_name, config.api_key, config.api_secret]):
                fixes.append("1. Set Cloudinary environment variables (CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET)")
        except ImportError:
            fixes.append("1. Install cloudinary and django-cloudinary-storage packages")
    
    # Check media URL configuration
    if not hasattr(settings, 'MEDIA_URL') or not settings.MEDIA_URL:
        fixes.append("2. Set MEDIA_URL in settings")
    
    # Check if using WhiteNoise fallback
    if not use_cloudinary and not getattr(settings, 'USE_S3', False):
        fixes.append("3. Configure WhiteNoise for media serving or enable Cloudinary")
    
    # Check DEBUG setting
    if getattr(settings, 'DEBUG', True):
        fixes.append("4. Set DEBUG=False in production")
    
    # Check ALLOWED_HOSTS
    allowed_hosts = getattr(settings, 'ALLOWED_HOSTS', [])
    if not allowed_hosts or allowed_hosts == ['*']:
        fixes.append("5. Set specific ALLOWED_HOSTS for production")
    
    if fixes:
        for fix in fixes:
            print(fix)
    else:
        print("No obvious configuration issues found.")
    
    print()
    print("Additional recommendations:")
    print("- Upload sample images via Django admin to test")
    print("- Check browser developer tools for 404 errors on images")
    print("- Verify Render environment variables are set correctly")

if __name__ == "__main__":
    print("Media Files Diagnostic Tool")
    print("===========================")
    print()
    
    check_django_settings()
    check_cloudinary_config()
    check_media_files()
    check_model_images()
    
    # Only test upload if Cloudinary is configured
    use_cloudinary = getattr(settings, 'USE_CLOUDINARY', False)
    if use_cloudinary:
        test_cloudinary_upload()
    
    suggest_fixes()
    
    print("Diagnosis complete!")
