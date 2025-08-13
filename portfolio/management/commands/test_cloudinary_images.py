"""
Django management command to test Cloudinary image configuration

Usage:
python manage.py test_cloudinary_images
"""

from django.core.management.base import BaseCommand
from django.conf import settings
from portfolio.models import Project, PersonalInfo, Testimonial, BlogPost
import os


class Command(BaseCommand):
    help = 'Test Cloudinary image configuration and URLs'

    def add_arguments(self, parser):
        parser.add_argument(
            '--fix-http',
            action='store_true',
            help='Attempt to fix any HTTP URLs to HTTPS',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Testing Cloudinary Images Configuration'))
        self.stdout.write('=' * 60)
        
        # Check settings
        self.stdout.write(f"\n1. Storage Configuration:")
        self.stdout.write(f"   DEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}")
        
        if 'cloudinary' not in settings.DEFAULT_FILE_STORAGE.lower():
            self.stdout.write(self.style.ERROR(
                "   ❌ Not using Cloudinary storage!"
            ))
            return
        
        # Test Cloudinary connection
        self.stdout.write(f"\n2. Cloudinary Connection:")
        try:
            import cloudinary
            import cloudinary.api
            
            result = cloudinary.api.ping()
            config = cloudinary.config()
            
            self.stdout.write(self.style.SUCCESS(f"   ✅ Connected to: {config.cloud_name}"))
            self.stdout.write(f"   Secure: {config.secure}")
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"   ❌ Connection failed: {e}"))
            return
        
        # Check image URLs
        self.stdout.write(f"\n3. Testing Image URLs:")
        
        total_images = 0
        cloudinary_images = 0
        broken_images = 0
        http_images = 0
        
        # Test project images
        projects = Project.objects.filter(image__isnull=False)
        for project in projects:
            total_images += 1
            try:
                url = project.image.url
                
                if url.startswith('https://res.cloudinary.com/'):
                    cloudinary_images += 1
                    self.stdout.write(f"   ✅ {project.title}: {url[:60]}...")
                elif url.startswith('http://res.cloudinary.com/'):
                    http_images += 1
                    self.stdout.write(self.style.WARNING(
                        f"   ⚠️ {project.title}: HTTP Cloudinary URL (should be HTTPS)"
                    ))
                    
                    if options['fix_http']:
                        # This is a demonstration - in practice, you'd need to 
                        # re-upload the image or update Cloudinary config
                        self.stdout.write(f"      🔧 Would fix HTTP URL for {project.title}")
                        
                else:
                    broken_images += 1
                    self.stdout.write(self.style.ERROR(
                        f"   ❌ {project.title}: Non-Cloudinary URL: {url[:60]}..."
                    ))
                    
            except Exception as e:
                broken_images += 1
                self.stdout.write(self.style.ERROR(f"   ❌ {project.title}: URL Error: {e}"))
        
        # Test other image types
        for model_name, model_class, image_field in [
            ('PersonalInfo', PersonalInfo, 'profile_image'),
            ('Testimonial', Testimonial, 'avatar'),
            ('BlogPost', BlogPost, 'image'),
        ]:
            objects = model_class.objects.filter(**{f"{image_field}__isnull": False})
            for obj in objects:
                total_images += 1
                try:
                    image = getattr(obj, image_field)
                    url = image.url
                    
                    if url.startswith('https://res.cloudinary.com/'):
                        cloudinary_images += 1
                        self.stdout.write(f"   ✅ {model_name}: {url[:60]}...")
                    elif url.startswith('http://res.cloudinary.com/'):
                        http_images += 1
                        self.stdout.write(self.style.WARNING(
                            f"   ⚠️ {model_name}: HTTP URL"
                        ))
                    else:
                        broken_images += 1
                        self.stdout.write(self.style.ERROR(
                            f"   ❌ {model_name}: Non-Cloudinary URL"
                        ))
                        
                except Exception as e:
                    broken_images += 1
                    self.stdout.write(self.style.ERROR(f"   ❌ {model_name}: {e}"))
        
        # Summary
        self.stdout.write(f"\n4. Summary:")
        self.stdout.write(f"   Total images: {total_images}")
        self.stdout.write(self.style.SUCCESS(f"   ✅ Working Cloudinary HTTPS: {cloudinary_images}"))
        
        if http_images > 0:
            self.stdout.write(self.style.WARNING(f"   ⚠️ HTTP Cloudinary URLs: {http_images}"))
            
        if broken_images > 0:
            self.stdout.write(self.style.ERROR(f"   ❌ Broken/Local URLs: {broken_images}"))
        
        # Recommendations
        self.stdout.write(f"\n5. Recommendations:")
        
        if broken_images > 0:
            self.stdout.write(self.style.WARNING(
                "   🔧 Re-upload broken images through Django admin"
            ))
        
        if http_images > 0:
            self.stdout.write(self.style.WARNING(
                "   🔧 Check Cloudinary secure=True configuration"
            ))
        
        if cloudinary_images == total_images:
            self.stdout.write(self.style.SUCCESS(
                "   🎉 All images are properly configured for Cloudinary!"
            ))
        
        # Test upload capability
        self.stdout.write(f"\n6. Testing Upload Capability:")
        try:
            from io import BytesIO
            from PIL import Image
            import cloudinary.uploader
            
            # Create a small test image
            test_img = Image.new('RGB', (50, 50), color='blue')
            buffer = BytesIO()
            test_img.save(buffer, format='PNG')
            buffer.seek(0)
            
            # Upload test
            upload_result = cloudinary.uploader.upload(
                buffer.getvalue(),
                public_id="django_test_image",
                folder="tests"
            )
            
            self.stdout.write(self.style.SUCCESS(
                f"   ✅ Upload successful: {upload_result['secure_url']}"
            ))
            
            # Clean up
            cloudinary.uploader.destroy("tests/django_test_image")
            self.stdout.write("   🧹 Test image cleaned up")
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"   ❌ Upload test failed: {e}"))
        
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write(self.style.SUCCESS('✅ Cloudinary test completed!'))
