#!/usr/bin/env python
"""
Script to fix project images by linking existing image files to projects
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_project.settings.dev')
django.setup()

from portfolio.models import Project
from django.conf import settings

def fix_project_images():
    print("=== FIXING PROJECT IMAGES ===")
    
    # Get all projects without images
    projects = Project.objects.filter(image='')
    
    # Available image files in the media directory
    media_projects_path = os.path.join(settings.MEDIA_ROOT, 'images', 'projects')
    available_images = []
    
    if os.path.exists(media_projects_path):
        for file in os.listdir(media_projects_path):
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                available_images.append(file)
    
    print(f"Found {len(projects)} projects without images")
    print(f"Found {len(available_images)} available image files")
    print()
    
    # Create a mapping for better matches
    image_mapping = {
        'E-commerce Dashboard': 'project_1.jpg',
        'Portfolio Website': 'project_2.jpg', 
        'CAR RENTAL SYSTEM': 'project_3.jpg',
        'Task Management System': 'test_project.jpg'
    }
    
    for project in projects:
        # Try to find a suitable image
        image_file = None
        
        # First, try the mapping
        if project.title in image_mapping:
            mapped_file = image_mapping[project.title]
            if mapped_file in available_images:
                image_file = mapped_file
        
        # If no mapped file, try to find one by name similarity
        if not image_file:
            for img in available_images:
                if not img.startswith('project_') or img.endswith('_kUXfeK9.jpg') or img.endswith('_wU629Ua.jpg') or img.endswith('_4RWn8Yi.jpg'):
                    continue
                image_file = img
                available_images.remove(img)  # Remove from available to avoid duplicates
                break
        
        if image_file:
            # Assign the image to the project
            project.image = f'images/projects/{image_file}'
            project.save()
            print(f"✅ Assigned '{image_file}' to '{project.title}'")
        else:
            print(f"❌ No suitable image found for '{project.title}'")
    
    print("\n=== VERIFICATION ===")
    projects_with_images = Project.objects.exclude(image='')
    for project in projects_with_images:
        image_path = os.path.join(settings.MEDIA_ROOT, project.image.name)
        exists = os.path.exists(image_path)
        print(f"Project: {project.title}")
        print(f"  Image: {project.image}")
        print(f"  URL: {project.image.url}")
        print(f"  File exists: {'✅' if exists else '❌'}")
        print()

if __name__ == '__main__':
    fix_project_images()
