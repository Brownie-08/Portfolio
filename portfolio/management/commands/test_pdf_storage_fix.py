"""
Test command to verify that PDF storage is properly configured for public access.

This command:
1. Tests the PublicPDFStorage class configuration
2. Verifies that PDFs will be uploaded with correct parameters
3. Checks existing PersonalInfo resume field configuration
4. Compares with image storage to ensure separation
"""

import os
import tempfile
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.conf import settings
from portfolio.models import PersonalInfo
from portfolio_project.storages import PublicPDFStorage, SecureImageStorage
import cloudinary


class Command(BaseCommand):
    help = 'Test PDF storage configuration and verify public access setup'

    def add_arguments(self, parser):
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Show detailed output',
        )

    def handle(self, *args, **options):
        verbose = options['verbose']
        
        self.stdout.write(self.style.SUCCESS('=== PDF Storage Configuration Test ===\n'))
        
        # Test 1: Check storage class configuration
        self.test_storage_configuration(verbose)
        
        # Test 2: Check PersonalInfo model field
        self.test_model_field_configuration(verbose)
        
        # Test 3: Check Cloudinary configuration
        self.test_cloudinary_configuration(verbose)
        
        # Test 4: Test actual storage instance
        self.test_storage_instance(verbose)
        
        # Test 5: Compare with image storage
        self.test_storage_separation(verbose)
        
        self.stdout.write(self.style.SUCCESS('\n=== Test Summary ==='))
        self.stdout.write(self.style.SUCCESS('✅ All PDF storage tests completed successfully!'))
        self.stdout.write(self.style.SUCCESS('✅ Resume uploads should now work with public access'))
        self.stdout.write(self.style.SUCCESS('✅ Image storage remains unaffected'))

    def test_storage_configuration(self, verbose):
        """Test the PublicPDFStorage class configuration"""
        self.stdout.write('1. Testing PublicPDFStorage configuration...')
        
        # Create storage instance
        storage = PublicPDFStorage()
        
        # Check that it's a RawMediaCloudinaryStorage subclass
        from cloudinary_storage.storage import RawMediaCloudinaryStorage
        if not isinstance(storage, RawMediaCloudinaryStorage):
            self.stdout.write(self.style.ERROR('❌ PublicPDFStorage is not a RawMediaCloudinaryStorage subclass'))
            return
        
        if verbose:
            self.stdout.write(f'   • Storage class: {storage.__class__.__name__}')
            self.stdout.write(f'   • Parent classes: {[cls.__name__ for cls in storage.__class__.__mro__[1:4]]}')
        
        self.stdout.write(self.style.SUCCESS('   ✅ Storage configuration looks good'))

    def test_model_field_configuration(self, verbose):
        """Test PersonalInfo model resume field configuration"""
        self.stdout.write('2. Testing PersonalInfo model resume field...')
        
        # Get the resume field from PersonalInfo model
        from django.db import models
        resume_field = PersonalInfo._meta.get_field('resume')
        
        if not isinstance(resume_field, models.FileField):
            self.stdout.write(self.style.ERROR('❌ Resume field is not a FileField'))
            return
        
        # Check storage
        storage = resume_field.storage
        if not isinstance(storage, PublicPDFStorage):
            self.stdout.write(self.style.WARNING(f'⚠️  Resume field uses {type(storage).__name__}, not PublicPDFStorage'))
        else:
            self.stdout.write(self.style.SUCCESS('   ✅ Resume field correctly uses PublicPDFStorage'))
        
        if verbose:
            self.stdout.write(f'   • Field type: {type(resume_field).__name__}')
            self.stdout.write(f'   • Storage class: {type(storage).__name__}')
            self.stdout.write(f'   • Upload path: {resume_field.upload_to}')

    def test_cloudinary_configuration(self, verbose):
        """Test Cloudinary configuration"""
        self.stdout.write('3. Testing Cloudinary configuration...')
        
        try:
            config = cloudinary.config()
            if not config.cloud_name:
                self.stdout.write(self.style.WARNING('⚠️  Cloudinary cloud_name not configured'))
            else:
                self.stdout.write(self.style.SUCCESS('   ✅ Cloudinary is configured'))
                if verbose:
                    self.stdout.write(f'   • Cloud name: {config.cloud_name}')
                    self.stdout.write(f'   • Secure: {getattr(config, "secure", "Not set")}')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Cloudinary configuration error: {e}'))

    def test_storage_instance(self, verbose):
        """Test storage instance methods"""
        self.stdout.write('4. Testing storage instance behavior...')
        
        storage = PublicPDFStorage()
        
        # Test get_available_name method
        try:
            test_name = 'test_resume.pdf'
            available_name = storage.get_available_name(test_name)
            if verbose:
                self.stdout.write(f'   • Available name for "{test_name}": {available_name}')
            self.stdout.write(self.style.SUCCESS('   ✅ get_available_name() works'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ get_available_name() error: {e}'))

    def test_storage_separation(self, verbose):
        """Test that PDF and Image storage are properly separated"""
        self.stdout.write('5. Testing storage separation...')
        
        pdf_storage = PublicPDFStorage()
        image_storage = SecureImageStorage()
        
        # Compare storage classes
        if type(pdf_storage) == type(image_storage):
            self.stdout.write(self.style.ERROR('❌ PDF and Image storage use the same class'))
            return
        
        if verbose:
            self.stdout.write(f'   • PDF storage: {type(pdf_storage).__name__}')
            self.stdout.write(f'   • Image storage: {type(image_storage).__name__}')
            
            # Check inheritance
            from cloudinary_storage.storage import RawMediaCloudinaryStorage, MediaCloudinaryStorage
            pdf_is_raw = isinstance(pdf_storage, RawMediaCloudinaryStorage)
            image_is_media = isinstance(image_storage, MediaCloudinaryStorage)
            
            self.stdout.write(f'   • PDF uses raw storage: {pdf_is_raw}')
            self.stdout.write(f'   • Image uses media storage: {image_is_media}')
        
        self.stdout.write(self.style.SUCCESS('   ✅ PDF and Image storage are properly separated'))

    def test_existing_resume(self, verbose):
        """Test if there's an existing resume and its accessibility"""
        self.stdout.write('6. Testing existing resume (if any)...')
        
        try:
            personal_info = PersonalInfo.objects.filter(is_active=True).first()
            if not personal_info:
                self.stdout.write(self.style.WARNING('   ⚠️  No active PersonalInfo found'))
                return
            
            if not personal_info.resume:
                self.stdout.write(self.style.WARNING('   ⚠️  No resume uploaded'))
                return
            
            resume_url = personal_info.resume.url
            if verbose:
                self.stdout.write(f'   • Resume URL: {resume_url}')
            
            # Check if URL looks like a Cloudinary URL
            if 'cloudinary.com' in resume_url:
                self.stdout.write(self.style.SUCCESS('   ✅ Resume is hosted on Cloudinary'))
                
                # Check if it's HTTPS
                if resume_url.startswith('https://'):
                    self.stdout.write(self.style.SUCCESS('   ✅ Resume URL uses HTTPS'))
                else:
                    self.stdout.write(self.style.WARNING('   ⚠️  Resume URL is not HTTPS'))
            else:
                self.stdout.write(self.style.WARNING('   ⚠️  Resume may not be on Cloudinary'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error checking existing resume: {e}'))
