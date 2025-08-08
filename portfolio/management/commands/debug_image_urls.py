#!/usr/bin/env python
"""
Quick diagnostic command to debug image URL issues in production
"""
from django.core.management.base import BaseCommand
from django.conf import settings
from portfolio.models import Project, PersonalInfo, Testimonial, Certification
import os


class Command(BaseCommand):
    help = 'Debug image URLs and storage configuration'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=== IMAGE URL DIAGNOSTIC ==='))
        
        # Check environment variables
        self.stdout.write('\n--- Environment Variables ---')
        use_cloudinary = os.environ.get('USE_CLOUDINARY', 'Not set')
        self.stdout.write(f'USE_CLOUDINARY: {use_cloudinary}')
        
        # Check Django settings
        self.stdout.write('\n--- Django Settings ---')
        self.stdout.write(f'DEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}')
        self.stdout.write(f'MEDIA_URL: {settings.MEDIA_URL}')
        
        # Check actual image URLs in database
        self.stdout.write('\n--- Project Images ---')
        for project in Project.objects.filter(image__isnull=False)[:3]:
            self.stdout.write(f'{project.title}: {project.image.name}')
            try:
                self.stdout.write(f'  URL: {project.image.url}')
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  URL Error: {e}'))
        
        self.stdout.write('\n--- Profile Images ---')
        for info in PersonalInfo.objects.filter(profile_image__isnull=False)[:1]:
            self.stdout.write(f'{info.full_name}: {info.profile_image.name}')
            try:
                self.stdout.write(f'  URL: {info.profile_image.url}')
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  URL Error: {e}'))
        
        self.stdout.write('\n--- Testimonial Avatars ---')
        for testimonial in Testimonial.objects.filter(avatar__isnull=False)[:2]:
            self.stdout.write(f'{testimonial.name}: {testimonial.avatar.name}')
            try:
                self.stdout.write(f'  URL: {testimonial.avatar.url}')
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  URL Error: {e}'))
