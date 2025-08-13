#!/usr/bin/env python
"""
Management command to fix resume file upload in Cloudinary with correct resource type
"""
from django.core.management.base import BaseCommand
from django.conf import settings
from portfolio.models import PersonalInfo


class Command(BaseCommand):
    help = 'Fix resume file in Cloudinary by re-uploading with correct resource type'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force re-upload even if current URL seems correct',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=== FIXING RESUME CLOUDINARY UPLOAD ===\n'))
        
        # Get personal info
        personal_info = PersonalInfo.objects.first()
        if not personal_info:
            self.stdout.write(self.style.ERROR('❌ No PersonalInfo found'))
            return
            
        if not personal_info.resume:
            self.stdout.write(self.style.ERROR('❌ No resume file found'))
            return
        
        self.stdout.write(f'✅ Found resume: {personal_info.resume.name}')
        
        # Check current URL
        try:
            current_url = personal_info.resume.url
            self.stdout.write(f'Current URL: {current_url}')
            
            # Check if URL has the wrong resource type
            if '/image/upload/' in current_url and not options['force']:
                self.stdout.write(self.style.WARNING('⚠️ Resume URL uses image/upload - needs fixing'))
            elif '/raw/upload/' in current_url and not options['force']:
                self.stdout.write(self.style.SUCCESS('✅ Resume URL already uses raw/upload - looks correct'))
                
                # Test if it actually works
                try:
                    import requests
                    response = requests.head(current_url, timeout=10)
                    if response.status_code == 200:
                        self.stdout.write(self.style.SUCCESS('✅ Current URL is working - no fix needed'))
                        return
                    else:
                        self.stdout.write(self.style.WARNING(f'⚠️ Current URL returns {response.status_code} - will fix'))
                except Exception:
                    self.stdout.write(self.style.WARNING('⚠️ Cannot test current URL - will fix anyway'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error getting current URL: {e}'))
        
        # Re-upload the file
        self.stdout.write('\n🔧 Re-uploading resume with correct settings...')
        
        try:
            import cloudinary.uploader
            import os
            
            # Read the current file content
            # Note: This reads from wherever the file is currently stored
            try:
                # Try to read file content
                resume_file = personal_info.resume
                with resume_file.open('rb') as f:
                    file_content = f.read()
                
                self.stdout.write(f'✅ Read {len(file_content)} bytes from resume file')
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'❌ Cannot read resume file: {e}'))
                self.stdout.write('💡 Try re-uploading the resume through Django admin instead')
                return
            
            # Get file extension
            file_name = personal_info.resume.name
            file_extension = os.path.splitext(file_name)[1].lower()
            
            # Create new public ID
            base_name = os.path.splitext(os.path.basename(file_name))[0]
            public_id = f"media/files/{base_name}"
            
            self.stdout.write(f'Using public_id: {public_id}')
            
            # Upload with correct settings for raw files
            result = cloudinary.uploader.upload(
                file_content,
                public_id=public_id,
                resource_type="raw",  # Correct resource type for PDFs
                access_mode="public",  # Ensure public access
                overwrite=True,  # Replace existing file
                invalidate=True,  # Clear CDN cache
                use_filename=False,  # Use our public_id
            )
            
            new_url = result.get('secure_url')
            self.stdout.write(self.style.SUCCESS('✅ Resume re-uploaded successfully!'))
            self.stdout.write(f'New URL: {new_url}')
            
            # Test the new URL
            try:
                import requests
                response = requests.head(new_url, timeout=10)
                if response.status_code == 200:
                    self.stdout.write(self.style.SUCCESS('✅ New URL is working correctly!'))
                else:
                    self.stdout.write(self.style.WARNING(f'⚠️ New URL returns {response.status_code}'))
            except Exception as e:
                self.stdout.write(f'Cannot test new URL: {e}')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Re-upload failed: {e}'))
            return
        
        self.stdout.write('\n' + '=' * 50)
        self.stdout.write(self.style.SUCCESS('✅ Resume fix completed!'))
        self.stdout.write('\n📝 Next steps:')
        self.stdout.write('1. Test the resume download from your live website')
        self.stdout.write('2. The URL should now work without 404 errors')
        self.stdout.write('3. If you upload a new resume later, it should work correctly')
