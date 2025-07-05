#!/usr/bin/env python3
"""
Script to fix media file issues for production deployment on Render.

This script ensures that all media files are properly available and 
that the application can serve them correctly in production.
"""

import os
import sys
import django
from pathlib import Path

# Setup Django
sys.path.append(str(Path(__file__).parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_project.settings.dev')
django.setup()

from django.conf import settings
from portfolio.models import PersonalInfo, Certification, Award, BlogPost, Project, Testimonial


def check_file_exists(file_field, description):
    """Check if a file field points to an existing file."""
    if not file_field:
        return False, f"❌ {description}: No file specified"
    
    try:
        file_path = file_field.path
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            return True, f"✅ {description}: {file_path} ({size} bytes)"
        else:
            return False, f"❌ {description}: File missing at {file_path}"
    except (ValueError, AttributeError) as e:
        return False, f"❌ {description}: Error accessing file - {e}"


def main():
    print("🔍 Checking media files for production deployment...\n")
    
    # Check media directory
    media_root = Path(settings.MEDIA_ROOT)
    if not media_root.exists():
        print(f"❌ Media directory does not exist: {media_root}")
        media_root.mkdir(parents=True, exist_ok=True)
        print(f"✅ Created media directory: {media_root}")
    else:
        print(f"✅ Media directory exists: {media_root}")
    
    print(f"📁 Media URL: {settings.MEDIA_URL}")
    print(f"📁 Media Root: {settings.MEDIA_ROOT}\n")
    
    # Check PersonalInfo files
    print("👤 Checking PersonalInfo files...")
    for info in PersonalInfo.objects.all():
        print(f"Profile for: {info.full_name}")
        
        # Check profile image
        exists, msg = check_file_exists(info.profile_image, "Profile Image")
        print(f"  {msg}")
        
        # Check resume
        exists, msg = check_file_exists(info.resume, "Resume/CV")
        print(f"  {msg}")
    
    # Check other model files
    models_to_check = [
        (Certification, 'certificate_image', 'Certificate Image'),
        (Award, 'award_image', 'Award Image'),
        (BlogPost, 'image', 'Blog Image'),
        (Project, 'image', 'Project Image'),
        (Testimonial, 'avatar', 'Testimonial Avatar'),
    ]
    
    for model, field_name, description in models_to_check:
        objects = model.objects.filter(**{f"{field_name}__isnull": False}).exclude(**{field_name: ''})
        if objects.exists():
            print(f"\n📋 Checking {model.__name__} files...")
            for obj in objects:
                file_field = getattr(obj, field_name)
                exists, msg = check_file_exists(file_field, f"{description} ({obj})")
                print(f"  {msg}")
    
    # List all files in media directory
    print(f"\n📂 All files in media directory:")
    if media_root.exists():
        for file_path in media_root.rglob('*'):
            if file_path.is_file():
                size = file_path.stat().st_size
                rel_path = file_path.relative_to(media_root)
                print(f"  📄 {rel_path} ({size} bytes)")
    else:
        print("  No media directory found!")
    
    # Check if media files are in git
    print(f"\n🔍 Checking if media files are tracked by git...")
    try:
        import subprocess
        result = subprocess.run(['git', 'ls-files', 'media/'], 
                              capture_output=True, text=True, cwd=str(Path(__file__).parent))
        if result.returncode == 0:
            if result.stdout.strip():
                print("✅ Media files are tracked by git:")
                for line in result.stdout.strip().split('\n'):
                    print(f"  📄 {line}")
            else:
                print("⚠️  No media files are tracked by git")
                print("   Consider adding important media files to git for deployment")
        else:
            print("❌ Could not check git status")
    except FileNotFoundError:
        print("❌ Git not found - skipping git check")
    
    print(f"\n✅ Media file check complete!")
    print(f"\n🚀 For Render deployment:")
    print(f"   1. Ensure media files are committed to git if needed")
    print(f"   2. MEDIA_URL and MEDIA_ROOT are properly configured")
    print(f"   3. WhiteNoise is serving media files in production")
    print(f"   4. URL patterns include media file serving")


if __name__ == "__main__":
    main()
