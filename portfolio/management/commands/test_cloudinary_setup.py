#!/usr/bin/env python
"""
Management command to test the complete Cloudinary setup including:
1. Environment variable configuration
2. Cloudinary connection
3. Image upload/download functionality
4. Selective storage (images to Cloudinary, resume files local)
5. Admin dashboard integration
"""
import os
import tempfile
from io import BytesIO
from PIL import Image
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile
from portfolio.models import Project, PersonalInfo


class Command(BaseCommand):
    help = 'Test complete Cloudinary setup and selective storage functionality'

    def add_arguments(self, parser):
        parser.add_argument(
            '--create-test-data',
            action='store_true',
            help='Create test project and personal info with images',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=== CLOUDINARY SETUP TEST ==='))
        
        # Test 1: Environment Configuration
        self._test_environment_config()
        
        # Test 2: Cloudinary Connection
        if not self._test_cloudinary_connection():
            return
        
        # Test 3: Direct Cloudinary Upload/Download
        self._test_direct_cloudinary_upload()
        
        # Test 4: Selective Storage Test
        self._test_selective_storage()
        
        # Test 5: Django Model Integration
        self._test_django_model_integration()
        
        # Test 6: Admin Dashboard (if requested)
        if options.get('create_test_data'):
            self._create_test_data()
        
        self.stdout.write(self.style.SUCCESS('\n=== ALL TESTS COMPLETED ==='))

    def _test_environment_config(self):
        """Test environment variable configuration"""
        self.stdout.write('\n--- Testing Environment Configuration ---')
        
        required_vars = [
            'USE_CLOUDINARY',
            'CLOUDINARY_CLOUD_NAME', 
            'CLOUDINARY_API_KEY',
            'CLOUDINARY_API_SECRET'
        ]
        
        all_set = True
        for var in required_vars:
            value = os.environ.get(var, 'Not set')
            if value == 'Not set':
                all_set = False
                self.stdout.write(self.style.ERROR(f'✗ {var}: {value}'))
            else:
                # Mask secrets for display
                if 'SECRET' in var or 'KEY' in var:
                    display_value = value[:8] + '***' if len(value) > 8 else '***'
                else:
                    display_value = value
                self.stdout.write(self.style.SUCCESS(f'✓ {var}: {display_value}'))
        
        if all_set:
            self.stdout.write(self.style.SUCCESS('✓ All environment variables are configured'))
        else:
            self.stdout.write(self.style.ERROR('✗ Some environment variables are missing'))
            self.stdout.write('Please update your .env file with Cloudinary credentials')
        
        # Test Django settings
        use_cloudinary = getattr(settings, 'USE_CLOUDINARY', False)
        if hasattr(settings, 'config'):
            try:
                use_cloudinary = settings.config('USE_CLOUDINARY', default=False, cast=bool)
            except:
                pass
        
        self.stdout.write(f'Django USE_CLOUDINARY setting: {use_cloudinary}')
        self.stdout.write(f'DEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}')
        
        return all_set

    def _test_cloudinary_connection(self):
        """Test Cloudinary API connection"""
        self.stdout.write('\n--- Testing Cloudinary Connection ---')
        
        try:
            import cloudinary
            import cloudinary.uploader
            import cloudinary.api
            
            # Test configuration
            config = cloudinary.config()
            self.stdout.write(f'✓ Cloud Name: {config.cloud_name}')
            self.stdout.write(f'✓ API Key: {config.api_key}')
            self.stdout.write(f'✓ Secure: {config.secure}')
            
            # Test API access
            cloudinary.api.ping()
            self.stdout.write(self.style.SUCCESS('✓ Cloudinary API connection successful'))
            return True
            
        except ImportError:
            self.stdout.write(self.style.ERROR('✗ Cloudinary not installed'))
            return False
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Cloudinary connection failed: {e}'))
            return False

    def _test_direct_cloudinary_upload(self):
        """Test direct upload to Cloudinary"""
        self.stdout.write('\n--- Testing Direct Cloudinary Upload ---')
        
        try:
            import cloudinary.uploader
            
            # Create test image
            img = Image.new('RGB', (200, 200), color='blue')
            img_io = BytesIO()
            img.save(img_io, format='JPEG')
            img_io.seek(0)
            
            # Upload to Cloudinary
            result = cloudinary.uploader.upload(
                img_io,
                public_id="portfolio_test_image",
                folder="test",
                resource_type="image",
                overwrite=True
            )
            
            self.stdout.write(self.style.SUCCESS('✓ Direct upload successful'))
            self.stdout.write(f'  URL: {result.get("secure_url")}')
            self.stdout.write(f'  Public ID: {result.get("public_id")}')
            
            # Clean up
            cloudinary.uploader.destroy("test/portfolio_test_image")
            self.stdout.write('✓ Test image cleaned up')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Direct upload failed: {e}'))

    def _test_selective_storage(self):
        """Test selective storage functionality"""
        self.stdout.write('\n--- Testing Selective Storage ---')
        
        try:
            from portfolio_project.storage import SelectiveCloudinaryStorage
            storage = SelectiveCloudinaryStorage()
            
            # Test image file (should use Cloudinary)
            test_cases = [
                ('images/test.jpg', 'Should use Cloudinary'),
                ('images/projects/test.png', 'Should use Cloudinary'),
                ('files/resume.pdf', 'Should use local storage'),
                ('files/my_resume.pdf', 'Should use local storage'),
                ('uploads/cv.pdf', 'Should use local storage'),
            ]
            
            for filename, expected in test_cases:
                should_local = storage._should_use_local(filename)
                storage_backend = 'Local' if should_local else 'Cloudinary'
                
                if ('resume' in filename.lower() or 'cv' in filename.lower() or filename.endswith('.pdf')):
                    expected_local = True
                else:
                    expected_local = False
                
                if should_local == expected_local:
                    self.stdout.write(self.style.SUCCESS(f'✓ {filename}: {storage_backend} ({expected})'))
                else:
                    self.stdout.write(self.style.ERROR(f'✗ {filename}: {storage_backend} (unexpected)'))
                    
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Selective storage test failed: {e}'))

    def _test_django_model_integration(self):
        """Test Django model integration with storage"""
        self.stdout.write('\n--- Testing Django Model Integration ---')
        
        try:
            # Test that models can be imported and have the expected fields
            self.stdout.write('✓ Project model imported successfully')
            self.stdout.write('✓ PersonalInfo model imported successfully')
            
            # Check field configurations
            project_image_field = Project._meta.get_field('image')
            personal_resume_field = PersonalInfo._meta.get_field('resume')
            personal_profile_field = PersonalInfo._meta.get_field('profile_image')
            
            self.stdout.write(f'✓ Project.image upload_to: {project_image_field.upload_to}')
            self.stdout.write(f'✓ PersonalInfo.resume upload_to: {personal_resume_field.upload_to}')
            self.stdout.write(f'✓ PersonalInfo.profile_image upload_to: {personal_profile_field.upload_to}')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Model integration test failed: {e}'))

    def _create_test_data(self):
        """Create test data for manual testing"""
        self.stdout.write('\n--- Creating Test Data ---')
        
        try:
            # Create test image
            img = Image.new('RGB', (300, 300), color='green')
            img_io = BytesIO()
            img.save(img_io, format='JPEG')
            img_io.seek(0)
            
            # Create test project with image
            test_image = SimpleUploadedFile(
                "test_project_image.jpg",
                img_io.getvalue(),
                content_type="image/jpeg"
            )
            
            project, created = Project.objects.get_or_create(
                slug='cloudinary-test-project',
                defaults={
                    'title': 'Cloudinary Test Project',
                    'description': 'Test project to verify Cloudinary integration',
                    'tech_stack': 'Django, Cloudinary',
                    'image': test_image,
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS('✓ Test project created with image'))
                self.stdout.write(f'  Image URL: {project.image.url}')
            else:
                self.stdout.write('Test project already exists')
            
            # Create test PDF resume
            pdf_content = b'%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Pages\n/Kids [3 0 R]\n/Count 1\n>>\nendobj\n3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/MediaBox [0 0 612 792]\n>>\nendobj\nxref\n0 4\n0000000000 65535 f \n0000000009 00000 n \n0000000074 00000 n \n0000000120 00000 n \ntrailer\n<<\n/Size 4\n/Root 1 0 R\n>>\nstartxref\n179\n%%EOF'
            
            test_resume = SimpleUploadedFile(
                "test_resume.pdf",
                pdf_content,
                content_type="application/pdf"
            )
            
            # Create or update PersonalInfo
            personal_info, created = PersonalInfo.objects.get_or_create(
                id=1,
                defaults={
                    'full_name': 'Test User',
                    'email': 'test@example.com',
                    'bio': 'Test bio for Cloudinary integration',
                    'resume': test_resume,
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS('✓ Test personal info created with resume'))
                self.stdout.write(f'  Resume URL: {personal_info.resume.url}')
            else:
                self.stdout.write('Test personal info already exists')
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Test data creation failed: {e}'))

    def _print_next_steps(self):
        """Print next steps for the user"""
        self.stdout.write('\n--- Next Steps ---')
        self.stdout.write('1. Update your .env file with actual Cloudinary credentials')
        self.stdout.write('2. Set USE_CLOUDINARY=True in production environment')
        self.stdout.write('3. Run the migration command: python manage.py migrate_images_to_cloudinary --dry-run')
        self.stdout.write('4. If dry-run looks good, run: python manage.py migrate_images_to_cloudinary')
        self.stdout.write('5. Deploy to Railway and test image display')
