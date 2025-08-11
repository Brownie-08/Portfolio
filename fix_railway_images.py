#!/usr/bin/env python
"""
Simple fix for Railway image issues
Run this in Railway terminal after ensuring Cloudinary is configured
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_project.settings.railway')
django.setup()

from django.conf import settings
from portfolio.models import Project, PersonalInfo, Testimonial

def fix_broken_images():
    print("=== FIXING RAILWAY IMAGE ISSUES ===\n")
    
    # Check if Cloudinary is properly configured
    use_cloudinary = os.environ.get('USE_CLOUDINARY', 'False').lower() in ('true', '1', 't')
    use_local_storage = os.environ.get('USE_LOCAL_STORAGE', 'True').lower() in ('true', '1', 't')
    
    print(f"USE_CLOUDINARY: {use_cloudinary}")
    print(f"USE_LOCAL_STORAGE: {use_local_storage}")
    print(f"Should use Cloudinary: {use_cloudinary and not use_local_storage}")
    
    if not (use_cloudinary and not use_local_storage):
        print("\n❌ CLOUDINARY NOT PROPERLY CONFIGURED!")
        print("Set these in Railway environment variables:")
        print("USE_CLOUDINARY=True")
        print("USE_LOCAL_STORAGE=False")
        print("CLOUDINARY_CLOUD_NAME=de9i7id2b")
        print("CLOUDINARY_API_KEY=547248818221456")
        print("CLOUDINARY_API_SECRET=611drBROvgh5Bkip4HZYaLRoddI")
        return
    
    print(f"\n✅ Cloudinary configuration looks correct")
    print(f"Storage backend: {settings.DEFAULT_FILE_STORAGE}")
    
    # Clear broken image references
    print(f"\n🧹 CLEARING BROKEN IMAGE REFERENCES:")
    
    # Clear projects with broken local images
    broken_projects = Project.objects.filter(image__isnull=False).exclude(image__icontains='cloudinary.com')
    print(f"Projects with local images: {broken_projects.count()}")
    for project in broken_projects:
        print(f"  - Clearing broken image from: {project.title}")
        project.image = None
        project.save()
    
    # Clear profile images with broken local paths
    personal_infos = PersonalInfo.objects.filter(profile_image__isnull=False).exclude(profile_image__icontains='cloudinary.com')
    print(f"Profile images with local paths: {personal_infos.count()}")
    for info in personal_infos:
        print(f"  - Clearing broken profile image from: {info.full_name}")
        info.profile_image = None
        info.save()
    
    # Clear testimonial avatars with broken local paths
    testimonials = Testimonial.objects.filter(avatar__isnull=False).exclude(avatar__icontains='cloudinary.com')
    print(f"Testimonial avatars with local paths: {testimonials.count()}")
    for testimonial in testimonials:
        print(f"  - Clearing broken avatar from: {testimonial.name}")
        testimonial.avatar = None
        testimonial.save()
    
    print(f"\n✅ CLEANUP COMPLETE!")
    print(f"\n📝 NEXT STEPS:")
    print(f"1. Go to your admin dashboard: /dashboard/")
    print(f"2. Upload NEW images - they will go to Cloudinary")
    print(f"3. New images will have URLs like: https://res.cloudinary.com/...")
    print(f"4. These images will PERSIST through redeployments!")

if __name__ == '__main__':
    fix_broken_images()
