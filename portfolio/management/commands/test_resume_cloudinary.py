#!/usr/bin/env python
"""
Management command to test resume file upload to Cloudinary
"""
from django.core.management.base import BaseCommand
from django.conf import settings
from portfolio.models import PersonalInfo


class Command(BaseCommand):
    help = 'Test resume file upload and URL generation with Cloudinary'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=== RESUME CLOUDINARY TEST ===\n'))
        
        # Check settings
        self.stdout.write('1. SETTINGS CHECK:')
        self.stdout.write(f'   DEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}')
        
        # Check if Cloudinary is properly configured
        if 'cloudinary' not in settings.DEFAULT_FILE_STORAGE.lower():
            self.stdout.write(self.style.ERROR('   ❌ Not using Cloudinary storage!'))
            return
        
        # Test Cloudinary connection
        self.stdout.write(f'\n2. CLOUDINARY CONNECTION:')
        try:
            import cloudinary
            import cloudinary.api
            
            result = cloudinary.api.ping()
            config = cloudinary.config()
            
            self.stdout.write(self.style.SUCCESS(f'   ✅ Connected to: {config.cloud_name}'))
            self.stdout.write(f'   Secure: {config.secure}')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   ❌ Connection failed: {e}'))
            return
        
        # Check resume files
        self.stdout.write(f'\n3. TESTING RESUME FILES:')
        
        personal_info = PersonalInfo.objects.first()
        if not personal_info:
            self.stdout.write(self.style.ERROR('   ❌ No PersonalInfo found'))
            return
            
        if not personal_info.resume:
            self.stdout.write(self.style.ERROR('   ❌ No resume file found'))
            return
        
        # Test resume URL generation
        try:
            resume_name = personal_info.resume.name
            self.stdout.write(f'   Resume name: {resume_name}')
            
            # Generate URL
            url = personal_info.resume.url
            self.stdout.write(f'   Resume URL: {url}')
            
            # Check if URL is Cloudinary
            if url.startswith('https://res.cloudinary.com/'):
                self.stdout.write(self.style.SUCCESS('   ✅ Cloudinary URL generated correctly'))
                
                # Test URL accessibility
                try:
                    import requests
                    response = requests.head(url, timeout=10)
                    if response.status_code == 200:
                        self.stdout.write(self.style.SUCCESS('   ✅ Resume file is accessible'))
                    elif response.status_code == 401:
                        self.stdout.write(self.style.ERROR('   ❌ Resume returns 401 Unauthorized'))
                        self.stdout.write('   💡 Fix: File needs public access_mode')
                    elif response.status_code == 404:
                        self.stdout.write(self.style.ERROR('   ❌ Resume returns 404 Not Found'))
                        self.stdout.write('   💡 Fix: File may not be uploaded to Cloudinary')
                    else:
                        self.stdout.write(self.style.WARNING(f'   ⚠️ Resume returns {response.status_code}'))
                        
                except ImportError:
                    self.stdout.write('   Cannot test URL accessibility (requests not available)')
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'   ⚠️ Error testing URL: {e}'))
                    
            elif url.startswith('/media/'):
                self.stdout.write(self.style.ERROR('   ❌ Local URL detected - will not work in Railway'))
                self.stdout.write('   💡 Fix: Ensure Cloudinary is configured correctly')
            else:
                self.stdout.write(self.style.WARNING(f'   ⚠️ Unknown URL format: {url}'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   ❌ Error generating resume URL: {e}'))
        
        # Test file upload capability
        self.stdout.write(f'\n4. TESTING FILE UPLOAD:')
        try:
            import cloudinary.uploader
            
            # Create a test PDF content
            test_content = b'%PDF-1.4\n1 0 obj\n<</Type /Catalog /Pages 2 0 R>>\nendobj\nxref\n0 2\n0000000000 65535 f \n0000000009 00000 n \ntrailer\n<</Size 2/Root 1 0 R>>\nstartxref\n44\n%%EOF'
            
            # Upload test PDF
            result = cloudinary.uploader.upload(
                test_content,
                public_id="test_resume",
                folder="media/files",
                resource_type="raw",  # For non-image files
                access_mode="public",
                overwrite=True
            )
            
            self.stdout.write(self.style.SUCCESS('   ✅ Test PDF uploaded successfully'))
            self.stdout.write(f'   Test URL: {result.get("secure_url")}')
            
            # Clean up test file
            cloudinary.uploader.destroy("media/files/test_resume", resource_type="raw")
            self.stdout.write('   🧹 Test file cleaned up')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   ❌ Upload test failed: {e}'))
        
        # Recommendations
        self.stdout.write(f'\n5. RECOMMENDATIONS:')
        
        if personal_info and personal_info.resume:
            try:
                url = personal_info.resume.url
                if url.startswith('https://res.cloudinary.com/'):
                    self.stdout.write(self.style.SUCCESS('   ✅ Resume is properly configured for Cloudinary'))
                    self.stdout.write('   📝 If still getting 404 in production:')
                    self.stdout.write('      1. Re-upload the resume through Django admin')
                    self.stdout.write('      2. Check Railway environment variables are set')
                    self.stdout.write('      3. Verify templates use {{ resume.url }} directly')
                else:
                    self.stdout.write(self.style.WARNING('   🔧 Re-upload resume through Django admin after deployment'))
                    
            except Exception:
                self.stdout.write(self.style.WARNING('   🔧 Re-upload resume through Django admin after deployment'))
        
        self.stdout.write('\n' + '=' * 50)
        self.stdout.write(self.style.SUCCESS('✅ Resume Cloudinary test completed!'))
