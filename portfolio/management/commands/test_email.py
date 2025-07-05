from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings


class Command(BaseCommand):
    help = 'Test email configuration'

    def add_arguments(self, parser):
        parser.add_argument(
            '--to',
            type=str,
            help='Email address to send test email to',
            default='emmanuelmikebrown242@yahoo.com'
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Testing email configuration...'))
        
        to_email = options['to']
        
        self.stdout.write(f'📧 Email Configuration:')
        self.stdout.write(f'  Backend: {settings.EMAIL_BACKEND}')
        self.stdout.write(f'  Host: {settings.EMAIL_HOST}')
        self.stdout.write(f'  Port: {settings.EMAIL_PORT}')
        self.stdout.write(f'  TLS: {settings.EMAIL_USE_TLS}')
        self.stdout.write(f'  From: {settings.DEFAULT_FROM_EMAIL}')
        self.stdout.write(f'  Contact Email: {getattr(settings, "CONTACT_EMAIL", "Not set")}')
        self.stdout.write(f'  To: {to_email}')
        
        try:
            self.stdout.write(f'\n📨 Sending test email...')
            
            send_mail(
                subject='Portfolio Contact Form Test',
                message='This is a test email from your portfolio contact form configuration.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[to_email],
                fail_silently=False,
            )
            
            self.stdout.write(
                self.style.SUCCESS('✅ Test email sent successfully!')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Email sending failed: {e}')
            )
            self.stdout.write(
                self.style.WARNING('\n💡 Common issues:')
            )
            self.stdout.write('  1. Check if Yahoo App Password is correct')
            self.stdout.write('  2. Ensure Two-Factor Authentication is enabled on Yahoo')
            self.stdout.write('  3. Verify SMTP settings are correct')
            self.stdout.write('  4. Check internet connection')
