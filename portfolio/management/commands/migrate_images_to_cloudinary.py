#!/usr/bin/env python
"""
Management command to migrate existing images from local media to Cloudinary
This script will:
1. Upload all local images to Cloudinary
2. Update database records to use Cloudinary URLs
3. Keep resume files local (as specified in requirements)
4. Provide detailed progress and error reporting
"""
import os
import logging
from pathlib import Path
from django.core.management.base import BaseCommand
from django.conf import settings
from portfolio.models import Project, Testimonial, BlogPost, PersonalInfo, Certification, Award, SEOSettings


class Command(BaseCommand):
    help = "Migrate existing images from local media to Cloudinary (keeps resume files local)"

    def __init__(self):
        super().__init__()
        self.migrated_count = 0
        self.failed_count = 0
        self.skipped_count = 0
        self.failed_items = []

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Run without making actual changes (preview mode)',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force re-upload of images that appear to be already on Cloudinary',
        )

    def handle(self, *args, **options):
        self.dry_run = options.get('dry_run', False)
        self.force = options.get('force', False)
        
        self.stdout.write(self.style.SUCCESS('=== CLOUDINARY IMAGE MIGRATION ==='))
        
        if self.dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No changes will be made'))
        
        # Check Cloudinary configuration
        if not self._check_cloudinary_config():
            return
        
        # Import Cloudinary after config check
        import cloudinary
        import cloudinary.uploader
        
        # Migrate images for each model
        self._migrate_project_images()
        self._migrate_testimonial_images()
        self._migrate_blog_images()
        self._migrate_personal_info_images()
        self._migrate_certification_images()
        self._migrate_award_images()
        self._migrate_seo_images()
        
        # Print summary
        self._print_summary()

    def _check_cloudinary_config(self):
        """Check if Cloudinary is properly configured"""
        try:
            import cloudinary
            import cloudinary.uploader
            import cloudinary.api
            
            # Check if environment variables are set
            required_vars = ['CLOUDINARY_CLOUD_NAME', 'CLOUDINARY_API_KEY', 'CLOUDINARY_API_SECRET']
            missing_vars = [var for var in required_vars if not os.environ.get(var)]
            
            if missing_vars:
                self.stdout.write(
                    self.style.ERROR(f'Missing Cloudinary environment variables: {", ".join(missing_vars)}')
                )
                self.stdout.write('Please set these variables in your .env file and production environment')
                return False
            
            # Test Cloudinary connection
            config = cloudinary.config()
            self.stdout.write(f'Cloud Name: {config.cloud_name}')
            self.stdout.write(self.style.SUCCESS('✓ Cloudinary configuration verified'))
            return True
            
        except ImportError:
            self.stdout.write(self.style.ERROR('✗ Cloudinary not installed. Run: pip install cloudinary django-cloudinary-storage'))
            return False
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Cloudinary configuration error: {e}'))
            return False

    def _migrate_project_images(self):
        """Migrate Project model images"""
        self.stdout.write('\n--- Migrating Project Images ---')
        projects = Project.objects.all()
        
        for project in projects:
            if project.image:
                self._migrate_image_field(project, 'image', f'projects/{project.slug}')

    def _migrate_testimonial_images(self):
        """Migrate Testimonial model avatars"""
        self.stdout.write('\n--- Migrating Testimonial Avatars ---')
        testimonials = Testimonial.objects.all()
        
        for testimonial in testimonials:
            if testimonial.avatar:
                self._migrate_image_field(testimonial, 'avatar', f'testimonials/{testimonial.id}')

    def _migrate_blog_images(self):
        """Migrate BlogPost model images"""
        self.stdout.write('\n--- Migrating Blog Images ---')
        blog_posts = BlogPost.objects.all()
        
        for post in blog_posts:
            if post.image:
                self._migrate_image_field(post, 'image', f'blog/{post.slug}')

    def _migrate_personal_info_images(self):
        """Migrate PersonalInfo model profile images (skip resume files)"""
        self.stdout.write('\n--- Migrating Personal Profile Images ---')
        personal_infos = PersonalInfo.objects.all()
        
        for info in personal_infos:
            if info.profile_image:
                self._migrate_image_field(info, 'profile_image', f'profile/{info.id}')
            
            # Skip resume files as per requirements
            if info.resume:
                self.stdout.write(f'Skipping resume file (keeping local): {info.resume.name}')
                self.skipped_count += 1

    def _migrate_certification_images(self):
        """Migrate Certification model images"""
        self.stdout.write('\n--- Migrating Certification Images ---')
        certifications = Certification.objects.all()
        
        for cert in certifications:
            if cert.certificate_image:
                self._migrate_image_field(cert, 'certificate_image', f'certifications/{cert.id}')

    def _migrate_award_images(self):
        """Migrate Award model images"""
        self.stdout.write('\n--- Migrating Award Images ---')
        awards = Award.objects.all()
        
        for award in awards:
            if award.award_image:
                self._migrate_image_field(award, 'award_image', f'awards/{award.id}')

    def _migrate_seo_images(self):
        """Migrate SEO model images"""
        self.stdout.write('\n--- Migrating SEO Images ---')
        seo_settings = SEOSettings.objects.all()
        
        for seo in seo_settings:
            if seo.og_image:
                self._migrate_image_field(seo, 'og_image', f'seo/{seo.page}')

    def _migrate_image_field(self, instance, field_name, cloudinary_folder):
        """Migrate a single image field to Cloudinary"""
        import cloudinary
        import cloudinary.uploader
        
        field = getattr(instance, field_name)
        if not field:
            return
        
        # Skip if already on Cloudinary (unless force is True)
        if not self.force and ('cloudinary' in str(field) or 'res.cloudinary.com' in str(field)):
            self.stdout.write(f'Already on Cloudinary: {instance} - {field_name}')
            self.skipped_count += 1
            return
        
        try:
            # Get the local file path
            if hasattr(field, 'path'):
                local_path = field.path
            else:
                # Handle cases where file might not have a local path
                local_path = os.path.join(settings.MEDIA_ROOT, field.name)
            
            if not os.path.exists(local_path):
                self.stdout.write(self.style.WARNING(f'File not found locally: {local_path}'))
                self.failed_count += 1
                self.failed_items.append(f'{instance} - {field_name}: File not found')
                return
            
            self.stdout.write(f'Uploading: {local_path}')
            
            if self.dry_run:
                self.stdout.write(f'[DRY RUN] Would upload: {local_path} to folder: {cloudinary_folder}')
                return
            
            # Upload to Cloudinary
            upload_result = cloudinary.uploader.upload(
                local_path,
                folder=cloudinary_folder,
                resource_type="auto",  # Let Cloudinary detect the resource type
                use_filename=True,
                unique_filename=True,
                overwrite=False
            )
            
            # Update the model field with Cloudinary URL
            setattr(instance, field_name, upload_result['secure_url'])
            instance.save(update_fields=[field_name])
            
            self.stdout.write(
                self.style.SUCCESS(f'✓ Migrated: {instance} - {field_name} -> {upload_result["secure_url"]}')
            )
            self.migrated_count += 1
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'✗ Failed to migrate {instance} - {field_name}: {e}')
            )
            self.failed_count += 1
            self.failed_items.append(f'{instance} - {field_name}: {str(e)}')

    def _print_summary(self):
        """Print migration summary"""
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS('MIGRATION SUMMARY'))
        self.stdout.write('='*50)
        self.stdout.write(f'Successfully migrated: {self.migrated_count} images')
        self.stdout.write(f'Skipped: {self.skipped_count} items')
        self.stdout.write(f'Failed: {self.failed_count} items')
        
        if self.failed_items:
            self.stdout.write('\nFailed items:')
            for item in self.failed_items:
                self.stdout.write(f'  - {item}')
        
        if self.dry_run:
            self.stdout.write(self.style.WARNING('\nThis was a DRY RUN - no changes were made'))
            self.stdout.write('Run without --dry-run to perform the actual migration')
        else:
            self.stdout.write(self.style.SUCCESS('\nMigration completed!'))
            if self.migrated_count > 0:
                self.stdout.write('Remember to:')
                self.stdout.write('1. Set USE_CLOUDINARY=True in your production environment')
                self.stdout.write('2. Deploy your application')
                self.stdout.write('3. Test that images display correctly')
