from django.core.management.base import BaseCommand
from django.conf import settings
from portfolio.models import PersonalInfo, Project


class Command(BaseCommand):
    help = 'Test Cloudinary configuration and debug media URLs'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Testing Cloudinary configuration...'))
        
        # Check Cloudinary settings
        self.stdout.write('\n=== CLOUDINARY SETTINGS ===')
        cloudinary_settings = [
            'USE_CLOUDINARY',
            'CLOUDINARY_CLOUD_NAME', 
            'CLOUDINARY_API_KEY',
            'CLOUDINARY_API_SECRET',
            'DEFAULT_FILE_STORAGE'
        ]
        
        for setting in cloudinary_settings:
            value = getattr(settings, setting, 'NOT SET')
            if 'SECRET' in setting and value != 'NOT SET':
                value = f"{value[:8]}***"  # Hide secret
            self.stdout.write(f'{setting}: {value}')
        
        # Test Cloudinary import
        self.stdout.write('\n=== CLOUDINARY IMPORT TEST ===')
        try:
            import cloudinary
            self.stdout.write(f'✅ Cloudinary module imported successfully')
            self.stdout.write(f'Cloudinary version: {cloudinary.__version__}')
            
            # Check cloudinary config
            config = cloudinary.config()
            self.stdout.write(f'Cloud name from config: {config.cloud_name}')
            self.stdout.write(f'API key from config: {config.api_key}')
            self.stdout.write(f'Secure setting: {config.secure}')
            
        except ImportError as e:
            self.stdout.write(self.style.ERROR(f'❌ Failed to import cloudinary: {e}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Cloudinary config error: {e}'))
        
        # Test media URLs
        self.stdout.write('\n=== MEDIA URLS TEST ===')
        try:
            personal_info = PersonalInfo.objects.first()
            if personal_info:
                self.stdout.write(f'Personal info found: {personal_info.full_name}')
                
                if personal_info.profile_image:
                    try:
                        url = personal_info.profile_image.url
                        self.stdout.write(f'Profile image URL: {url}')
                        self.stdout.write(f'Profile image name: {personal_info.profile_image.name}')
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'❌ Error getting profile image URL: {e}'))
                else:
                    self.stdout.write('No profile image found')
                    
                if personal_info.resume:
                    try:
                        url = personal_info.resume.url
                        self.stdout.write(f'Resume URL: {url}')
                        self.stdout.write(f'Resume name: {personal_info.resume.name}')
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'❌ Error getting resume URL: {e}'))
                else:
                    self.stdout.write('No resume found')
            else:
                self.stdout.write('No PersonalInfo objects found')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error testing PersonalInfo: {e}'))
        
        # Test project images
        self.stdout.write('\n=== PROJECT IMAGES TEST ===')
        try:
            projects = Project.objects.filter(image__isnull=False)[:3]
            for project in projects:
                try:
                    url = project.image.url
                    self.stdout.write(f'Project "{project.title}" image URL: {url}')
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'❌ Error getting image URL for {project.title}: {e}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error testing projects: {e}'))
        
        self.stdout.write(self.style.SUCCESS('\nCloudinary test complete!'))
