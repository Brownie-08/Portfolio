#!/usr/bin/env python
"""
Simple fix for Cloudinary URLs that are stored as full URLs in the database
This ensures they display correctly without Django prepending /media/
"""
from django.core.management.base import BaseCommand
from portfolio.models import Project, PersonalInfo, Testimonial, Certification, Award, SEOSettings


class Command(BaseCommand):
    help = 'Fix Cloudinary URLs that are stored as full URLs'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=== FIXING CLOUDINARY URLs ==='))
        
        fixed_count = 0
        
        # Fix Project images
        self.stdout.write('\n--- Fixing Project Images ---')
        for project in Project.objects.filter(image__isnull=False):
            if project.image.name.startswith('https://res.cloudinary.com/'):
                # Extract just the path part for proper Django URL handling
                cloudinary_path = project.image.name.replace('https://res.cloudinary.com/', '')
                project.image.name = cloudinary_path
                project.save(update_fields=['image'])
                self.stdout.write(f'✓ Fixed: {project.title}')
                fixed_count += 1
        
        # Fix Testimonial avatars
        self.stdout.write('\n--- Fixing Testimonial Avatars ---')
        for testimonial in Testimonial.objects.filter(avatar__isnull=False):
            if testimonial.avatar.name.startswith('https://res.cloudinary.com/'):
                cloudinary_path = testimonial.avatar.name.replace('https://res.cloudinary.com/', '')
                testimonial.avatar.name = cloudinary_path
                testimonial.save(update_fields=['avatar'])
                self.stdout.write(f'✓ Fixed: {testimonial.name}')
                fixed_count += 1
        
        # Fix PersonalInfo profile images
        self.stdout.write('\n--- Fixing Profile Images ---')
        for info in PersonalInfo.objects.filter(profile_image__isnull=False):
            if info.profile_image.name.startswith('https://res.cloudinary.com/'):
                cloudinary_path = info.profile_image.name.replace('https://res.cloudinary.com/', '')
                info.profile_image.name = cloudinary_path
                info.save(update_fields=['profile_image'])
                self.stdout.write(f'✓ Fixed: {info.full_name} profile')
                fixed_count += 1
        
        # Fix Certification images  
        self.stdout.write('\n--- Fixing Certification Images ---')
        for cert in Certification.objects.filter(certificate_image__isnull=False):
            if cert.certificate_image.name.startswith('https://res.cloudinary.com/'):
                cloudinary_path = cert.certificate_image.name.replace('https://res.cloudinary.com/', '')
                cert.certificate_image.name = cloudinary_path
                cert.save(update_fields=['certificate_image'])
                self.stdout.write(f'✓ Fixed: {cert.name}')
                fixed_count += 1
        
        # Fix other models...
        self.stdout.write('\n--- Fixing Other Images ---')
        for award in Award.objects.filter(award_image__isnull=False):
            if award.award_image.name.startswith('https://res.cloudinary.com/'):
                cloudinary_path = award.award_image.name.replace('https://res.cloudinary.com/', '')
                award.award_image.name = cloudinary_path
                award.save(update_fields=['award_image'])
                self.stdout.write(f'✓ Fixed: {award.title}')
                fixed_count += 1
        
        for seo in SEOSettings.objects.filter(og_image__isnull=False):
            if seo.og_image.name.startswith('https://res.cloudinary.com/'):
                cloudinary_path = seo.og_image.name.replace('https://res.cloudinary.com/', '')
                seo.og_image.name = cloudinary_path
                seo.save(update_fields=['og_image'])
                self.stdout.write(f'✓ Fixed: SEO {seo.page}')
                fixed_count += 1
        
        self.stdout.write(f'\n✅ Fixed {fixed_count} image URLs')
        self.stdout.write('Images should now display correctly with Cloudinary!')
