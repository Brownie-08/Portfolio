from django.core.management.base import BaseCommand
from django.conf import settings
from django.urls import reverse
from portfolio.models import PersonalInfo
import os
import requests


class Command(BaseCommand):
    help = 'Test media file serving and URL generation'

    def add_arguments(self, parser):
        parser.add_argument(
            '--test-urls', 
            action='store_true',
            help='Test actual URL accessibility (requires running server)'
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Testing media file serving...'))
        
        # Check basic settings
        self.stdout.write('\n=== MEDIA SETTINGS ===')
        self.stdout.write(f'DEBUG: {settings.DEBUG}')
        self.stdout.write(f'MEDIA_URL: {getattr(settings, "MEDIA_URL", "NOT SET")}')
        self.stdout.write(f'MEDIA_ROOT: {getattr(settings, "MEDIA_ROOT", "NOT SET")}')
        self.stdout.write(f'DEFAULT_FILE_STORAGE: {getattr(settings, "DEFAULT_FILE_STORAGE", "NOT SET")}')
        
        # Test personal info media files
        self.stdout.write('\n=== PERSONAL INFO MEDIA FILES ===')
        try:
            personal_info = PersonalInfo.objects.first()
            if personal_info:
                self.stdout.write(f'Personal info found: {personal_info.full_name}')
                
                # Test profile image
                if personal_info.profile_image:
                    self._test_file_field(personal_info.profile_image, 'Profile Image')
                else:
                    self.stdout.write('No profile image found')
                
                # Test resume
                if personal_info.resume:
                    self._test_file_field(personal_info.resume, 'Resume')
                else:
                    self.stdout.write('No resume found')
                    
            else:
                self.stdout.write('No PersonalInfo objects found')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error testing PersonalInfo: {e}'))
        
        # Test template tag URL generation
        self.stdout.write('\n=== TEMPLATE TAG TESTING ===')
        try:
            from portfolio.templatetags.portfolio_extras import profile_image_url
            if personal_info and personal_info.profile_image:
                url = profile_image_url(personal_info)
                self.stdout.write(f'Template tag profile_image_url result: {url}')
                
                if url and options['test_urls']:
                    self._test_url_accessibility(url)
            else:
                self.stdout.write('No profile image to test template tag with')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error testing template tags: {e}'))
        
        # Test fallback URLs
        self.stdout.write('\n=== FALLBACK URL TESTING ===')
        try:
            profile_serve_url = reverse('portfolio:serve_profile_image')
            self.stdout.write(f'Profile serve fallback URL: {profile_serve_url}')
            
            if options['test_urls']:
                self._test_url_accessibility(profile_serve_url)
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error testing fallback URLs: {e}'))
        
        self.stdout.write(self.style.SUCCESS('\nMedia serving test complete!'))
    
    def _test_file_field(self, file_field, name):
        """Test a file field for existence and URL generation"""
        self.stdout.write(f'\n--- Testing {name} ---')
        self.stdout.write(f'File name: {file_field.name}')
        
        # Check if file physically exists
        try:
            if hasattr(file_field, 'path'):
                file_path = file_field.path
                exists = os.path.exists(file_path)
                self.stdout.write(f'Physical file exists: {exists}')
                if exists:
                    size = os.path.getsize(file_path)
                    self.stdout.write(f'File size: {size} bytes')
                else:
                    self.stdout.write(f'File path: {file_path}')
        except Exception as e:
            self.stdout.write(f'Could not check physical file: {e}')
        
        # Check URL generation
        try:
            url = file_field.url
            self.stdout.write(f'Generated URL: {url}')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error generating URL: {e}'))
    
    def _test_url_accessibility(self, url):
        """Test if a URL is accessible (requires server to be running)"""
        try:
            # Only test relative URLs by making them absolute
            if url.startswith('/'):
                # Assume localhost for testing
                test_url = f'http://localhost:8000{url}'
            else:
                test_url = url
            
            self.stdout.write(f'Testing URL accessibility: {test_url}')
            response = requests.get(test_url, timeout=5)
            self.stdout.write(f'Response status: {response.status_code}')
            
            if response.status_code == 200:
                self.stdout.write(self.style.SUCCESS('✓ URL is accessible'))
            else:
                self.stdout.write(self.style.WARNING(f'⚠ URL returned status {response.status_code}'))
                
        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.WARNING(f'Could not test URL accessibility: {e}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error testing URL: {e}'))
