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

        self.stdout.write(f"🔧 Attempting to create superuser with username: {username}")

        # Check if user already exists
        if User.objects.filter(username=username).exists():
            if not options['force']:
                self.stdout.write(
                    self.style.WARNING(f"⚠️  User '{username}' already exists. Use --force to recreate.")
                )
                return
            else:
                # Delete existing user if --force is used
                User.objects.filter(username=username).delete()
                self.stdout.write(f"🗑️  Existing user '{username}' deleted.")

        try:
            # Create the superuser
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            
            self.stdout.write(
                self.style.SUCCESS(f"✅ Superuser '{username}' created successfully!")
            )
            self.stdout.write(f"📧 Email: {email}")
            self.stdout.write(f"🔗 Login at: /admin/")
            self.stdout.write(f"🌐 Environment variables used:")
            self.stdout.write(f"   DJANGO_SUPERUSER_USERNAME={username}")
            self.stdout.write(f"   DJANGO_SUPERUSER_EMAIL={email}")
            self.stdout.write(f"   DJANGO_SUPERUSER_PASSWORD={'*' * len(password)}")
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Failed to create superuser: {e}")
            )
