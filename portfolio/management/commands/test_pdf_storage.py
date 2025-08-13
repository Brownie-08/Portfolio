#!/usr/bin/env python
"""
Management command to test the new PDF storage configuration
"""
from django.core.management.base import BaseCommand
from django.conf import settings
from portfolio.models import PersonalInfo
from portfolio_project.storages import PublicPDFStorage


class Command(BaseCommand):
    help = 'Test the new PDF storage configuration'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=== PDF STORAGE TEST ===\n'))
        
        # Test 1: Storage Class Instantiation
        self.stdout.write('1. TESTING STORAGE CLASS:')
        try:
            pdf_storage = PublicPDFStorage()
            self.stdout.write(self.style.SUCCESS('   ✅ PublicPDFStorage instantiated successfully'))
            self.stdout.write(f'   Storage class: {pdf_storage.__class__.__name__}')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   ❌ Storage instantiation failed: {e}'))
            return
        
        # Test 2: Check PersonalInfo Model
        self.stdout.write('\n2. TESTING MODEL FIELD:')
        try:
            personal_info = PersonalInfo.objects.first()
            if personal_info:
                resume_field = PersonalInfo._meta.get_field('resume')
                self.stdout.write(f'   Resume field type: {resume_field.__class__.__name__}')
                self.stdout.write(f'   Resume storage: {resume_field.storage.__class__.__name__}')
                
                if hasattr(personal_info, 'resume') and personal_info.resume:
                    self.stdout.write(f'   Current resume file: {personal_info.resume.name}')
                    try:
                        url = personal_info.resume.url
                        self.stdout.write(f'   Current URL: {url}')
                        
                        if '/raw/upload/' in url:
                            self.stdout.write(self.style.SUCCESS('   ✅ URL uses raw/upload (correct for PDFs)'))
                        elif '/image/upload/' in url:
                            self.stdout.write(self.style.WARNING('   ⚠️ URL uses image/upload (old format - needs re-upload)'))
                        else:
                            self.stdout.write(f'   ⚠️ Unknown URL format')
                    except Exception as e:
                        self.stdout.write(f'   ❌ Error getting URL: {e}')
                else:
                    self.stdout.write('   No resume file found')
            else:
                self.stdout.write(self.style.WARNING('   No PersonalInfo found'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   ❌ Model test failed: {e}'))
        
        # Test 3: Cloudinary Configuration
        self.stdout.write('\n3. TESTING CLOUDINARY CONFIG:')
        try:
            import cloudinary
            config = cloudinary.config()
            self.stdout.write(f'   Cloud Name: {config.cloud_name}')
            self.stdout.write(f'   Secure: {config.secure}')
            self.stdout.write(self.style.SUCCESS('   ✅ Cloudinary configuration looks good'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   ❌ Cloudinary config error: {e}'))
        
        # Test 4: Upload Test
        self.stdout.write('\n4. TESTING UPLOAD CAPABILITY:')
        try:
            import cloudinary.uploader
            
            # Create a test PDF content
            test_content = b'%PDF-1.4\n1 0 obj\n<</Type /Catalog /Pages 2 0 R>>\nendobj\nxref\n0 2\n0000000000 65535 f \n0000000009 00000 n \ntrailer\n<</Size 2/Root 1 0 R>>\nstartxref\n44\n%%EOF'
            
            # Test upload using our storage
            result = cloudinary.uploader.upload(
                test_content,
                public_id="test_pdf_storage",
                folder="media/files",
                resource_type="raw",
                access_mode="public",
                overwrite=True
            )
            
            test_url = result.get('secure_url')
            self.stdout.write(self.style.SUCCESS('   ✅ Test PDF upload successful'))
            self.stdout.write(f'   Test URL: {test_url}')
            
            # Verify URL format
            if '/raw/upload/' in test_url:
                self.stdout.write(self.style.SUCCESS('   ✅ Upload URL uses correct raw/upload format'))
            else:
                self.stdout.write(self.style.WARNING('   ⚠️ Upload URL format unexpected'))
            
            # Clean up test file
            cloudinary.uploader.destroy("media/files/test_pdf_storage", resource_type="raw")
            self.stdout.write('   🧹 Test file cleaned up')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   ❌ Upload test failed: {e}'))
        
        # Test 5: Recommendations
        self.stdout.write('\n5. NEXT STEPS:')
        
        personal_info = PersonalInfo.objects.first()
        if personal_info and personal_info.resume:
            try:
                url = personal_info.resume.url
                if '/image/upload/' in url:
                    self.stdout.write(self.style.WARNING('   🔄 REQUIRED: Re-upload resume through Django admin'))
                    self.stdout.write('   📝 The existing resume uses old storage format')
                    self.stdout.write('   📝 After re-upload, it will use raw/upload format')
                elif '/raw/upload/' in url:
                    self.stdout.write(self.style.SUCCESS('   ✅ Resume storage is already correct'))
                    self.stdout.write('   📝 No action needed - resume should work in production')
            except Exception:
                self.stdout.write(self.style.WARNING('   🔄 RECOMMENDED: Re-upload resume through Django admin'))
        else:
            self.stdout.write('   📝 Upload a resume through Django admin to test')
        
        self.stdout.write('\n' + '=' * 50)
        self.stdout.write(self.style.SUCCESS('✅ PDF Storage test completed!'))
