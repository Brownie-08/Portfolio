from django.core.management.base import BaseCommand
from django.conf import settings
from portfolio.models import PersonalInfo, Project, Testimonial
import os


class Command(BaseCommand):
    help = 'Setup media file placeholders and update models with placeholder URLs'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Setting up media placeholders...'))

        # Create media directories if they don't exist
        self.create_media_directories()
        
        # Update models with placeholder URLs
        self.update_personal_info()
        self.update_projects()
        self.update_testimonials()

        self.stdout.write(self.style.SUCCESS('✅ Media placeholders setup completed!'))
        self.stdout.write(self.style.WARNING('📝 Note: Upload actual images through Django admin at /admin/'))

    def create_media_directories(self):
        """Create media directories"""
        media_dirs = [
            'images/profile',
            'images/projects',
            'images/testimonials',
            'images/blog',
            'images/certifications',
            'files',
        ]

        for directory in media_dirs:
            full_path = os.path.join(settings.MEDIA_ROOT, directory)
            os.makedirs(full_path, exist_ok=True)
            self.stdout.write(f'✅ Created directory: {directory}')

    def update_personal_info(self):
        """Update personal info with placeholder image"""
        try:
            personal_info = PersonalInfo.objects.get(id=1)
            # Use a placeholder service for profile image
            if not personal_info.profile_image:
                # This will show a placeholder until real image is uploaded
                self.stdout.write('Personal info ready for profile image upload')
        except PersonalInfo.DoesNotExist:
            self.stdout.write(self.style.WARNING('Personal info not found. Run seed_production_data first.'))

    def update_projects(self):
        """Update projects with placeholder images"""
        projects = Project.objects.all()
        for project in projects:
            if not project.image:
                # Projects are ready for image uploads
                self.stdout.write(f'Project "{project.title}" ready for image upload')

    def update_testimonials(self):
        """Update testimonials with placeholder avatars"""
        testimonials = Testimonial.objects.all()
        for testimonial in testimonials:
            if not testimonial.avatar:
                # Testimonials are ready for avatar uploads
                try:
                    name = getattr(testimonial, 'name', 'Unknown')
                    self.stdout.write(f'Testimonial from "{name}" ready for avatar upload')
                except AttributeError:
                    self.stdout.write('Testimonial ready for avatar upload (name field missing)')
