from django.core.management.base import BaseCommand
from portfolio.models import PersonalInfo

class Command(BaseCommand):
    help = 'Set up initial personal information'

    def add_arguments(self, parser):
        parser.add_argument('--name', type=str, help='Your full name')
        parser.add_argument('--portfolio-name', type=str, help='Portfolio brand name', default='My Portfolio')
        parser.add_argument('--email', type=str, help='Your email address')
        parser.add_argument('--bio', type=str, help='Your bio/about text')

    def handle(self, *args, **options):
        self.stdout.write('Setting up personal information...')
        
        # Interactive input if not provided
        full_name = options.get('name') or input('Enter your full name: ')
        portfolio_name = options.get('portfolio_name') or input('Enter portfolio name (default: My Portfolio): ') or 'My Portfolio'
        email = options.get('email') or input('Enter your email: ')
        bio = options.get('bio') or input('Enter a short bio: ') or 'Passionate developer creating innovative solutions.'
        
        # Create or update personal info
        personal_info, created = PersonalInfo.objects.get_or_create(
            is_active=True,
            defaults={
                'portfolio_name': portfolio_name,
                'full_name': full_name,
                'email': email,
                'bio': bio,
            }
        )
        
        if not created:
            # Update existing info
            personal_info.portfolio_name = portfolio_name
            personal_info.full_name = full_name
            personal_info.email = email
            personal_info.bio = bio
            personal_info.save()
            self.stdout.write(
                self.style.WARNING(f'Updated personal information for {full_name}')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f'Created personal information for {full_name}')
            )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Portfolio will now be branded as "{portfolio_name}"'
            )
        )
