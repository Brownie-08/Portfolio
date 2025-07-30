#!/usr/bin/env python
"""
Debug script to check project image paths and media serving
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_project.settings.dev')
django.setup()

from portfolio.models import Project
from django.conf import settings

print("=== DEBUGGING PROJECT IMAGES ===")
print(f"Media Root: {settings.MEDIA_ROOT}")
print(f"Media URL: {settings.MEDIA_URL}")
print()

print("=== ALL PROJECTS ===")
projects = Project.objects.all()
for project in projects:
    print(f"\nProject: {project.title}")
    print(f"  Slug: {project.slug}")
    print(f"  Image Field: {project.image}")
    print(f"  Image Name: {project.image.name if project.image else 'No image'}")
    
    if project.image:
        print(f"  Image URL: {project.image.url}")
        image_path = os.path.join(settings.MEDIA_ROOT, project.image.name)
        print(f"  Full Path: {image_path}")
        print(f"  Exists: {os.path.exists(image_path)}")
        if os.path.exists(image_path):
            print(f"  Size: {os.path.getsize(image_path)} bytes")

print("\n=== MEDIA DIRECTORY CONTENTS ===")
media_projects_path = os.path.join(settings.MEDIA_ROOT, 'images', 'projects')
if os.path.exists(media_projects_path):
    files = os.listdir(media_projects_path)
    print(f"Files in {media_projects_path}:")
    for file in files:
        print(f"  - {file}")
else:
    print(f"Directory {media_projects_path} does not exist!")

print("\n=== SETTINGS CHECK ===")
print(f"DEBUG: {settings.DEBUG}")
print(f"ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
