from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from portfolio.models import ContactMessage


class Command(BaseCommand):
    help = 'Test email functionality for the contact form'

    def add_arguments(self, parser):
        parser.add_argument(
            '--to',
            type=str,
            help='Email address to send test email to',
            default=getattr(settings, 'CONTACT_EMAIL', settings.DEFAULT_FROM_EMAIL)
        )

    def handle(self, *args, **options):
        self.stdout.write('Testing email functionality...')
        
        try:
            # Test basic email sending
            send_mail(
                subject='Test Email from Portfolio Contact Form',
                message='This is a test email to verify that your email configuration is working correctly.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[options['to']],
                fail_silently=False,
            )
            
            self.stdout.write(
                self.style.SUCCESS(f'✓ Test email sent successfully to {options["to"]}')
            )
            
            # Display current email configuration
            self.stdout.write('\nCurrent email configuration:')
            self.stdout.write(f'  EMAIL_BACKEND: {settings.EMAIL_BACKEND}')
            self.stdout.write(f'  EMAIL_HOST: {getattr(settings, "EMAIL_HOST", "Not set")}')
            self.stdout.write(f'  EMAIL_PORT: {getattr(settings, "EMAIL_PORT", "Not set")}')
            self.stdout.write(f'  EMAIL_USE_TLS: {getattr(settings, "EMAIL_USE_TLS", "Not set")}')
            self.stdout.write(f'  DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}')
            self.stdout.write(f'  CONTACT_EMAIL: {getattr(settings, "CONTACT_EMAIL", "Not set")}')
            self.stdout.write(f'  SEND_AUTO_REPLY: {getattr(settings, "SEND_AUTO_REPLY", "Not set")}')
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'✗ Failed to send test email: {e}')
            )
            self.stdout.write('Please check your email configuration in settings.py or .env file')
