"""
Django management command to test resume download functionality.

This command helps diagnose issues with resume file serving in production.
"""

from django.core.management.base import BaseCommand
from django.urls import reverse
from django.conf import settings
from portfolio.models import PersonalInfo
import os
import requests


class Command(BaseCommand):
    help = 'Test resume download functionality and diagnose issues'

    def add_arguments(self, parser):
        parser.add_argument(
            '--check-file',
            action='store_true',
            help='Check if resume file exists on disk',
        )
        parser.add_argument(
            '--test-url',
            action='store_true',
            help='Test resume URL accessibility',
        )
        parser.add_argument(
            '--show-info',
            action='store_true',
            help='Show resume file information',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=== Resume Download Test ===\n'))
        
        # Get personal info
        personal_info = PersonalInfo.get_active()
        
        if not personal_info:
            self.stdout.write(self.style.ERROR('❌ No active PersonalInfo found'))
            return
            
        self.stdout.write(f'✅ Found PersonalInfo: {personal_info.full_name}')
        
        if not personal_info.resume:
            self.stdout.write(self.style.ERROR('❌ No resume file attached to PersonalInfo'))
            return
            
        self.stdout.write(f'✅ Resume field has file: {personal_info.resume.name}')
        
        # Show file info
        if options.get('show_info', True):
            self.show_file_info(personal_info.resume)
        
        # Check file existence
        if options.get('check_file', True):
            self.check_file_existence(personal_info.resume)
        
        # Test URL generation
        if options.get('test_url', True):
            self.test_url_generation(personal_info)

    def show_file_info(self, resume_field):
        """Show information about the resume file."""
        self.stdout.write(self.style.SUCCESS('\n--- File Information ---'))
        
        try:
            self.stdout.write(f'File name: {resume_field.name}')
            self.stdout.write(f'File size: {resume_field.size} bytes')
            
            try:
                self.stdout.write(f'File path: {resume_field.path}')
            except (ValueError, AttributeError) as e:
                self.stdout.write(f'File path error: {e}')
            
            try:
                self.stdout.write(f'File URL: {resume_field.url}')
            except (ValueError, AttributeError) as e:
                self.stdout.write(f'File URL error: {e}')
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error getting file info: {e}'))

    def check_file_existence(self, resume_field):
        """Check if the resume file exists on disk."""
        self.stdout.write(self.style.SUCCESS('\n--- File Existence Check ---'))
        
        try:
            # Check if file exists using path
            try:
                file_path = resume_field.path
                exists = os.path.exists(file_path)
                if exists:
                    self.stdout.write(f'✅ File exists at: {file_path}')
                    # Check if readable
                    if os.access(file_path, os.R_OK):
                        self.stdout.write('✅ File is readable')
                    else:
                        self.stdout.write(self.style.WARNING('⚠️  File is not readable'))
                else:
                    self.stdout.write(self.style.ERROR(f'❌ File does not exist at: {file_path}'))
            except (ValueError, AttributeError) as e:
                self.stdout.write(f'Path check failed: {e}')
                
                # Try alternative method
                if hasattr(resume_field, 'name') and resume_field.name:
                    file_path = os.path.join(settings.MEDIA_ROOT, resume_field.name)
                    exists = os.path.exists(file_path)
                    if exists:
                        self.stdout.write(f'✅ File exists at constructed path: {file_path}')
                    else:
                        self.stdout.write(self.style.ERROR(f'❌ File does not exist at constructed path: {file_path}'))
                        
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error checking file existence: {e}'))

    def test_url_generation(self, personal_info):
        """Test URL generation and accessibility."""
        self.stdout.write(self.style.SUCCESS('\n--- URL Generation Test ---'))
        
        # Test direct URL
        try:
            direct_url = personal_info.resume.url
            self.stdout.write(f'Direct URL: {direct_url}')
        except Exception as e:
            self.stdout.write(f'Direct URL failed: {e}')
        
        # Test template tag URL
        try:
            from portfolio.templatetags.portfolio_extras import resume_download_url
            template_url = resume_download_url(personal_info)
            self.stdout.write(f'Template tag URL: {template_url}')
        except Exception as e:
            self.stdout.write(f'Template tag URL failed: {e}')
        
        # Test reverse URLs
        try:
            serve_url = reverse('portfolio:serve_resume')
            self.stdout.write(f'Serve resume URL: {serve_url}')
        except Exception as e:
            self.stdout.write(f'Serve resume URL failed: {e}')
            
        try:
            download_url = reverse('portfolio:download_resume')
            self.stdout.write(f'Download resume URL: {download_url}')
        except Exception as e:
            self.stdout.write(f'Download resume URL failed: {e}')
        
        # Show storage settings
        self.stdout.write(self.style.SUCCESS('\n--- Storage Configuration ---'))
        self.stdout.write(f'MEDIA_ROOT: {getattr(settings, "MEDIA_ROOT", "Not set")}')
        self.stdout.write(f'MEDIA_URL: {getattr(settings, "MEDIA_URL", "Not set")}')
        self.stdout.write(f'DEFAULT_FILE_STORAGE: {getattr(settings, "DEFAULT_FILE_STORAGE", "Not set")}')
        self.stdout.write(f'USE_CLOUDINARY: {getattr(settings, "USE_CLOUDINARY", False)}')
        
        self.stdout.write(self.style.SUCCESS('\n=== Test Complete ==='))
