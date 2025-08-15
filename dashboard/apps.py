from django.apps import AppConfig
import os


class DashboardConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "dashboard"

    def ready(self):
        """Create superuser automatically if one doesn't exist."""
        # Import here to avoid Django startup issues
        from django.contrib.auth.models import User
        from django.core.management.color import no_style
        from django.db import connection
        
        try:
            # Check if database tables exist first
            table_names = connection.introspection.table_names()
            if 'auth_user' not in table_names:
                print("⚠️  Database tables not yet created. Skipping superuser creation.")
                return
                
            # Get superuser credentials from environment variables
            username = os.getenv("DJANGO_SUPERUSER_USERNAME", "admin")
            email = os.getenv("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
            password = os.getenv("DJANGO_SUPERUSER_PASSWORD", "adminpass123")
            
            # Check if superuser already exists
            if not User.objects.filter(username=username).exists():
                User.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password
                )
                print(f"✅ Superuser '{username}' created automatically for Railway deployment!")
                print(f"📧 Email: {email}")
                print(f"🔗 Admin URL: /admin/")
            else:
                print(f"ℹ️  Superuser '{username}' already exists.")
                
        except Exception as e:
            print(f"⚠️  Superuser creation skipped: {e}")
            # Don't raise the exception to avoid breaking the app startup
