from django.core.management.base import BaseCommand
from django.conf import settings
import os
import shutil
from portfolio.models import PersonalInfo


class Command(BaseCommand):
    help = 'Prepare media files for production deployment'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Preparing media files for production...'))
        
        # Ensure media directory exists
        if not os.path.exists(settings.MEDIA_ROOT):
            os.makedirs(settings.MEDIA_ROOT)
            self.stdout.write(f'Created media directory: {settings.MEDIA_ROOT}')
        
        # Check for PersonalInfo objects with media files
        info_objects = PersonalInfo.objects.all()
        
        for info in info_objects:
            # Check profile image
            if info.profile_image:
                profile_path = info.profile_image.path
                if os.path.exists(profile_path):
                    self.stdout.write(f'✅ Profile image exists: {profile_path}')
                else:
                    self.stdout.write(self.style.WARNING(f'❌ Profile image missing: {profile_path}'))
            
            # Check resume file
            if info.resume:
                resume_path = info.resume.path
                if os.path.exists(resume_path):
                    self.stdout.write(f'✅ Resume file exists: {resume_path}')
                else:
                    self.stdout.write(self.style.WARNING(f'❌ Resume file missing: {resume_path}'))
        
        # List all files in media directory
        self.stdout.write('\nMedia directory contents:')
        if os.path.exists(settings.MEDIA_ROOT):
            for root, dirs, files in os.walk(settings.MEDIA_ROOT):
                level = root.replace(str(settings.MEDIA_ROOT), '').count(os.sep)
                indent = ' ' * 2 * level
                self.stdout.write(f'{indent}{os.path.basename(root)}/')
                subindent = ' ' * 2 * (level + 1)
                for file in files:
                    file_path = os.path.join(root, file)
                    file_size = os.path.getsize(file_path)
                    self.stdout.write(f'{subindent}{file} ({file_size} bytes)')
        else:
            self.stdout.write('Media directory does not exist!')
        
        self.stdout.write(self.style.SUCCESS('\nMedia preparation complete!'))
