"""
Management command to fix Cloudinary resume file permissions.

This command re-uploads the resume file to Cloudinary with proper public access.
"""

import os
from django.core.management.base import BaseCommand
from django.conf import settings
from portfolio.models import PersonalInfo


class Command(BaseCommand):
    help = 'Fix Cloudinary resume file permissions for public access'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force-reupload',
            action='store_true',
            help='Force re-upload of resume file to Cloudinary',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=== Fixing Cloudinary Resume Access ===\n'))
        
        # Check if Cloudinary is configured
        if not getattr(settings, 'USE_CLOUDINARY', False):
            self.stdout.write(self.style.ERROR('❌ Cloudinary is not configured'))
            return
            
        try:
            import cloudinary
            import cloudinary.uploader
            import cloudinary.api
        except ImportError:
            self.stdout.write(self.style.ERROR('❌ Cloudinary package not available'))
            return
        
        # Get personal info
        personal_info = PersonalInfo.get_active()
        
        if not personal_info:
            self.stdout.write(self.style.ERROR('❌ No active PersonalInfo found'))
            return
            
        if not personal_info.resume:
            self.stdout.write(self.style.ERROR('❌ No resume file found in PersonalInfo'))
            return
            
        self.stdout.write(f'✅ Found resume file: {personal_info.resume.name}')
        
        # Check current file access
        self.check_current_access(personal_info)
        
        # Fix the file permissions
        if options['force_reupload']:
            self.fix_file_permissions(personal_info)
        else:
            self.fix_existing_file_permissions(personal_info)

    def check_current_access(self, personal_info):
        """Check current file access status."""
        self.stdout.write(self.style.SUCCESS('\n--- Current File Access Status ---'))
        
        try:
            # Try to access the file URL
            url = personal_info.resume.url
            self.stdout.write(f'Current URL: {url}')
            
            # Test URL accessibility
            try:
                import requests
                response = requests.head(url, timeout=10)
                if response.status_code == 200:
                    self.stdout.write(self.style.SUCCESS('✅ File is accessible'))
                elif response.status_code == 401:
                    self.stdout.write(self.style.ERROR('❌ File returns 401 Unauthorized'))
                elif response.status_code == 403:
                    self.stdout.write(self.style.ERROR('❌ File returns 403 Forbidden'))
                else:
                    self.stdout.write(self.style.WARNING(f'⚠️  File returns {response.status_code}'))
            except ImportError:
                self.stdout.write('Cannot test URL access (requests not available)')
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error checking file access: {e}'))

    def fix_existing_file_permissions(self, personal_info):
        """Fix permissions for existing file without re-uploading."""
        self.stdout.write(self.style.SUCCESS('\n--- Fixing Existing File Permissions ---'))
        
        try:
            import cloudinary.api
            
            # Get the public ID from the file
            file_name = personal_info.resume.name
            if file_name.startswith('media/'):
                file_name = file_name[6:]
            public_id = os.path.splitext(file_name)[0]
            
            self.stdout.write(f'Public ID: {public_id}')
            
            # Update the resource to make it public
            result = cloudinary.api.update(
                public_id,
                resource_type="raw",
                type="upload",
                access_mode="public"
            )
            
            self.stdout.write(self.style.SUCCESS(f'✅ Updated file permissions: {result.get("secure_url", "Success")}'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error fixing permissions: {e}'))
            self.stdout.write('Try using --force-reupload to re-upload the file')

    def fix_file_permissions(self, personal_info):
        """Fix permissions by re-uploading the file."""
        self.stdout.write(self.style.SUCCESS('\n--- Re-uploading File with Public Access ---'))
        
        try:
            import cloudinary.uploader
            
            # Get file content
            resume_file = personal_info.resume
            
            # Use a clean public ID
            base_name = os.path.splitext(os.path.basename(resume_file.name))[0]
            public_id = f"media/files/{base_name}"
            
            self.stdout.write(f'Using public ID: {public_id}')
            
            # Upload with public access
            with resume_file.open('rb') as file_content:
                result = cloudinary.uploader.upload(
                    file_content,
                    public_id=public_id,
                    resource_type="raw",
                    type="upload",
                    access_mode="public",
                    overwrite=True,
                    invalidate=True,
                    use_filename=True,
                    unique_filename=False
                )
            
            new_url = result.get('secure_url')
            self.stdout.write(self.style.SUCCESS('✅ File re-uploaded successfully!'))
            self.stdout.write(f'New URL: {new_url}')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error re-uploading file: {e}'))
        
        self.stdout.write(self.style.SUCCESS('\n=== Fix Complete ==='))
        self.stdout.write('\n📝 Next steps:')
        self.stdout.write('1. Test the resume download from your website')
        self.stdout.write('2. If still not working, try accessing the Cloudinary URL directly')
        self.stdout.write('3. Check your Cloudinary dashboard for file permissions')
