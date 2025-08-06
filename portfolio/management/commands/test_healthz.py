from django.core.management.base import BaseCommand
from django.test import Client
from django.urls import reverse


class Command(BaseCommand):
    help = 'Test the health check endpoint'

    def handle(self, *args, **options):
        client = Client()
        
        try:
            # Test the healthz endpoint
            response = client.get('/healthz/')
            self.stdout.write(
                self.style.SUCCESS(
                    f'Health check returned status {response.status_code}: {response.content.decode()}'
                )
            )
            
            if response.status_code == 200:
                self.stdout.write(self.style.SUCCESS('✅ Health check endpoint is working!'))
            else:
                self.stdout.write(self.style.ERROR('❌ Health check endpoint failed!'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Health check failed with error: {e}'))
