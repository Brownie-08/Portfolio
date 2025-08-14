"""
Management command to create an admin user for Railway production deployment.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.management import CommandError
import os


class Command(BaseCommand):
    help = 'Create an admin superuser for Railway production deployment'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            default='admin',
            help='Username for the admin user (default: admin)'
        )
        parser.add_argument(
            '--email',
            type=str,
            default='admin@portfolio.com',
            help='Email for the admin user'
        )
        parser.add_argument(
            '--password',
            type=str,
            help='Password for the admin user (if not provided, will use environment variable)'
        )
        parser.add_argument(
            '--noinput',
            action='store_true',
            help='Do not prompt for input (use for production deployment)'
        )

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']
        noinput = options['noinput']

        # Try to get password from environment variable if not provided
        if not password:
            password = os.environ.get('DJANGO_ADMIN_PASSWORD')

        # Check if user already exists
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'Admin user "{username}" already exists. Skipping creation.')
            )
            return

        # If no password and not in noinput mode, prompt for it
        if not password and not noinput:
            password = input(f'Enter password for admin user "{username}": ')

        # Validate password
        if not password:
            raise CommandError(
                'Password is required. Either provide --password, set DJANGO_ADMIN_PASSWORD '
                'environment variable, or run without --noinput to be prompted.'
            )

        try:
            # Create the superuser
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created admin user: "{username}"')
            )
            self.stdout.write(
                self.style.SUCCESS(f'Email: {email}')
            )
            self.stdout.write(
                self.style.SUCCESS('Admin user can now access /admin/ panel')
            )

        except Exception as e:
            raise CommandError(f'Error creating admin user: {e}')


# Usage examples:
# python manage.py createadmin --username=myuser --email=my@email.com --password=mypass
# python manage.py createadmin --noinput  # Uses environment variables
# DJANGO_ADMIN_PASSWORD=mypass python manage.py createadmin --noinput
