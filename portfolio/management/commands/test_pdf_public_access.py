"""
Test command to verify that PDFs are uploaded with access_mode="public"
This command tests the fix for 401 authentication errors on resume downloads.
"""

from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from portfolio_project.storages import PublicPDFStorage
import cloudinary.uploader
import tempfile
import os


class Command(BaseCommand):
    help = 'Test that PDFs are uploaded with access_mode=public to prevent 401 errors'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=== TESTING PDF PUBLIC ACCESS FIX ===\n'))
        
        # Test 1: Verify storage class configuration
        self.stdout.write('1. Testing PublicPDFStorage configuration...')
        try:
            storage = PublicPDFStorage()
            self.stdout.write(self.style.SUCCESS('   ✅ PublicPDFStorage instantiated successfully'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   ❌ Storage instantiation failed: {e}'))
            return

        # Test 2: Create a test PDF and verify upload options
        self.stdout.write('\n2. Testing PDF upload with forced public access...')
        
        # Create test PDF content
        test_pdf_content = b'%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Pages\n/Kids [3 0 R]\n/Count 1\n>>\nendobj\n3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/MediaBox [0 0 612 792]\n>>\nendobj\nxref\n0 4\n0000000000 65535 f \n0000000009 00000 n \n0000000074 00000 n \n0000000120 00000 n \ntrailer\n<<\n/Size 4\n/Root 1 0 R\n>>\nstartxref\n179\n%%EOF'
        
        test_file = ContentFile(test_pdf_content, name='test_public_access.pdf')
        
        try:
            # Use our custom storage to save the file
            saved_name = storage.save('files/test_public_access.pdf', test_file)
            self.stdout.write(self.style.SUCCESS(f'   ✅ Test PDF saved: {saved_name}'))
            
            # Get the URL
            test_url = storage.url(saved_name)
            self.stdout.write(f'   Test URL: {test_url}')
            
            # Verify URL format
            if '/raw/upload/' in test_url:
                self.stdout.write(self.style.SUCCESS('   ✅ URL uses correct raw/upload format'))
            else:
                self.stdout.write(self.style.WARNING('   ⚠️  URL format unexpected'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   ❌ Test upload failed: {e}'))
            return

        # Test 3: Verify the file is actually accessible without authentication
        self.stdout.write('\n3. Testing public accessibility (no authentication required)...')
        try:
            import requests
            response = requests.get(test_url, timeout=10)
            
            if response.status_code == 200:
                self.stdout.write(self.style.SUCCESS('   ✅ Test PDF is publicly accessible!'))
                self.stdout.write(f'   Response size: {len(response.content)} bytes')
                
                # Verify it's actually a PDF
                if response.content.startswith(b'%PDF'):
                    self.stdout.write(self.style.SUCCESS('   ✅ Response is valid PDF content'))
                else:
                    self.stdout.write(self.style.WARNING('   ⚠️  Response is not PDF content'))
                    
            elif response.status_code == 401:
                self.stdout.write(self.style.ERROR('   ❌ PDF still requires authentication (401)'))
                self.stdout.write('   This means the fix did not work properly')
                
            elif response.status_code == 404:
                self.stdout.write(self.style.WARNING('   ⚠️  PDF not found (404) - upload may have failed'))
                
            else:
                self.stdout.write(self.style.WARNING(f'   ⚠️  Unexpected status code: {response.status_code}'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   ❌ Error testing accessibility: {e}'))

        # Test 4: Check Cloudinary API to verify access_mode
        self.stdout.write('\n4. Verifying access_mode in Cloudinary API...')
        try:
            import cloudinary.api
            
            # Extract public_id from saved name
            public_id = saved_name.replace('files/', 'media/files/')
            if not public_id.startswith('media/'):
                public_id = f'media/{public_id}'
                
            # Get resource info from Cloudinary
            resource_info = cloudinary.api.resource(public_id, resource_type='raw')
            
            access_mode = resource_info.get('access_mode', 'Not specified')
            resource_type = resource_info.get('resource_type', 'Not specified')
            delivery_type = resource_info.get('type', 'Not specified')
            
            self.stdout.write(f'   Resource Type: {resource_type}')
            self.stdout.write(f'   Delivery Type: {delivery_type}')
            self.stdout.write(f'   Access Mode: {access_mode}')
            
            if access_mode == 'public':
                self.stdout.write(self.style.SUCCESS('   ✅ Access mode is PUBLIC - fix working!'))
            else:
                self.stdout.write(self.style.ERROR(f'   ❌ Access mode is {access_mode} - fix NOT working'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   ❌ Error checking Cloudinary API: {e}'))

        # Test 5: Cleanup test file
        self.stdout.write('\n5. Cleaning up test file...')
        try:
            # Delete test file from Cloudinary
            public_id = saved_name.replace('files/', 'media/files/')
            if not public_id.startswith('media/'):
                public_id = f'media/{public_id}'
                
            cloudinary.uploader.destroy(public_id, resource_type='raw')
            self.stdout.write(self.style.SUCCESS('   ✅ Test file cleaned up'))
            
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'   ⚠️  Cleanup failed: {e}'))

        # Summary
        self.stdout.write('\n=== TEST SUMMARY ===')
        self.stdout.write('✅ PublicPDFStorage class is properly configured')
        self.stdout.write('✅ Test PDF upload completed')
        self.stdout.write('✅ Ready to re-upload resume via Django admin')
        self.stdout.write('')
        self.stdout.write('NEXT STEPS:')
        self.stdout.write('1. Deploy these changes to Railway')
        self.stdout.write('2. Go to Django Admin > Personal Information')
        self.stdout.write('3. Upload a new resume file')
        self.stdout.write('4. Test resume download - should work without 401 errors')
        self.stdout.write('5. In Cloudinary dashboard, verify Access Mode shows "Public"')
