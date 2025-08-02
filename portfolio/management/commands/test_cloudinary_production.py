#!/usr/bin/env python
"""
Management command to test Cloudinary configuration and image handling
"""
import os
import tempfile
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files.base import ContentFile
from PIL import Image
import io


class Command(BaseCommand):
    help = 'Test Cloudinary configuration and image upload'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=== CLOUDINARY PRODUCTION TEST ==='))
        
        # Check if Cloudinary is configured
        use_cloudinary = getattr(settings, 'USE_CLOUDINARY', False)
        if hasattr(settings, 'config'):
            try:
                use_cloudinary = settings.config('USE_CLOUDINARY', default=False, cast=bool)
            except:
                pass
        
        self.stdout.write(f'USE_CLOUDINARY: {use_cloudinary}')
        
        # Check environment variables
        env_vars = [
            'USE_CLOUDINARY',
            'CLOUDINARY_CLOUD_NAME', 
            'CLOUDINARY_API_KEY',
            'CLOUDINARY_API_SECRET'
        ]
        
        self.stdout.write('\n=== Environment Variables ===')
        for var in env_vars:
            value = os.environ.get(var, 'Not set')
            if 'SECRET' in var and value != 'Not set':
                value = value[:5] + '***'
            self.stdout.write(f'{var}: {value}')
        
        # Test Cloudinary import
        self.stdout.write('\n=== Testing Cloudinary Import ===')
        try:
            import cloudinary
            import cloudinary.uploader
            import cloudinary.api
            self.stdout.write(self.style.SUCCESS('✓ Cloudinary imports successful'))
            
            # Check configuration
            config = cloudinary.config()
            self.stdout.write(f'Cloud Name: {config.cloud_name}')
            self.stdout.write(f'API Key: {config.api_key}')
            self.stdout.write(f'Secure: {config.secure}')
            
        except ImportError as e:
            self.stdout.write(self.style.ERROR(f'✗ Cloudinary import failed: {e}'))
            return
        
        # Test image upload
        self.stdout.write('\n=== Testing Image Upload ===')
        try:
            # Create a simple test image
            img = Image.new('RGB', (100, 100), color='red')
            img_io = io.BytesIO()
            img.save(img_io, format='JPEG')
            img_io.seek(0)
            
            # Upload to Cloudinary
            result = cloudinary.uploader.upload(
                img_io,
                public_id="test_image_portfolio",
                resource_type="image",
                overwrite=True
            )
            
            self.stdout.write(self.style.SUCCESS('✓ Image uploaded successfully'))
            self.stdout.write(f'URL: {result.get("secure_url")}')
            self.stdout.write(f'Public ID: {result.get("public_id")}')
            
            # Clean up - delete test image
            cloudinary.uploader.destroy("test_image_portfolio")
            self.stdout.write(self.style.SUCCESS('✓ Test image cleaned up'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Image upload failed: {e}'))
        
        # Test Django integration
        self.stdout.write('\n=== Testing Django Integration ===')
        try:
            from portfolio.models import Project
            
            # Check if we can create a project with an image field
            self.stdout.write('✓ Model import successful')
            self.stdout.write(f'DEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Django integration test failed: {e}'))
        
        self.stdout.write(self.style.SUCCESS('\n=== Test Complete ==='))
