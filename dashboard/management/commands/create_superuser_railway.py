"""
Custom management command to create superuser from environment variables.
This is a backup method if the automatic creation in apps.py doesn't work.

Usage:
python manage.py create_superuser_railway
"""

import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Creates a superuser from Railway environment variables'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force create superuser even if one already exists with the same username'
        )

    def handle(self, *args, **options):
        # Get credentials from environment variables
        username = os.getenv("DJANGO_SUPERUSER_USERNAME", "admin")
        email = os.getenv("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
        password = os.getenv("DJANGO_SUPERUSER_PASSWORD", "adminpass123")

        self.stdout.write(f"🔧 Creating/updating superuser with username: {username}")

        try:
            # Use get_or_create to handle both creation and updates
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "email": email,
                    "is_staff": True,
                    "is_superuser": True,
                }
            )
            
            # Always update critical fields (similar to apps.py logic)
            user.email = email
            user.is_staff = True
            user.is_superuser = True
            user.set_password(password)  # Force reset password
            user.save()
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"✅ Superuser '{username}' created successfully!")
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(f"✅ Superuser '{username}' updated with fresh credentials!")
                )
                
            self.stdout.write(f"📧 Email: {email}")
            self.stdout.write(f"🔗 Login at: /admin/")
            self.stdout.write(f"🎯 Password updated from Railway environment variables")
            self.stdout.write(f"🌐 Environment variables used:")
            self.stdout.write(f"   DJANGO_SUPERUSER_USERNAME={username}")
            self.stdout.write(f"   DJANGO_SUPERUSER_EMAIL={email}")
            self.stdout.write(f"   DJANGO_SUPERUSER_PASSWORD={'*' * len(password)}")
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Failed to create/update superuser: {e}")
            )
