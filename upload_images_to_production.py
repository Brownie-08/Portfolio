#!/usr/bin/env python
"""
Script to upload existing local images to production via dashboard
This script will help you re-upload images after Cloudinary is configured
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_project.settings.dev')
django.setup()

from portfolio.models import Project
from django.conf import settings

def show_image_upload_guide():
    print("=== IMAGE UPLOAD GUIDE FOR PRODUCTION ===")
    print()
    print("After setting up Cloudinary, you'll need to re-upload your project images.")
    print("Here's what to do:")
    print()
    print("1. Go to your production dashboard: https://your-portfolio-url.onrender.com/dashboard/login/")
    print("2. Login with your credentials")
    print("3. Navigate to Projects section")
    print("4. Edit each project and upload the image")
    print()
    print("Your local project images are located at:")
    
    media_projects_path = os.path.join(settings.MEDIA_ROOT, 'images', 'projects')
    if os.path.exists(media_projects_path):
        for file in os.listdir(media_projects_path):
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                print(f"  - {file}")
    
    print()
    print("Current projects in database:")
    projects = Project.objects.all()
    for project in projects:
        print(f"  - {project.title}")
        if project.image:
            print(f"    Current image: {project.image}")
        else:
            print(f"    No image assigned")
    
    print()
    print("💡 TIP: You can drag and drop images from your local media/images/projects/")
    print("folder directly into the dashboard forms!")

if __name__ == '__main__':
    show_image_upload_guide()
