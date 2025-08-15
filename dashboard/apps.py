from django.apps import AppConfig
import os


class DashboardConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "dashboard"

    def ready(self):
        """Create or update superuser automatically on every deployment."""
        # Import here to avoid Django startup issues
        from django.contrib.auth import get_user_model
        from django.db import connection
        
        try:
            # Check if database tables exist first
            table_names = connection.introspection.table_names()
            if 'auth_user' not in table_names:
                print("⚠️  Database tables not yet created. Skipping superuser creation.")
                return
                
            self.create_or_update_superuser()
                
        except Exception as e:
            print(f"⚠️  Superuser creation/update skipped: {e}")
            # Don't raise the exception to avoid breaking the app startup
            
    def create_or_update_superuser(self):
        """Create or update superuser with current environment variables."""
        from django.contrib.auth import get_user_model
        
        User = get_user_model()
        
        # Get superuser credentials from environment variables
        username = os.getenv("DJANGO_SUPERUSER_USERNAME", "admin")
        email = os.getenv("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
        password = os.getenv("DJANGO_SUPERUSER_PASSWORD", "adminpass123")
        
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
            
            # Always update critical fields on every deployment
            user.email = email
            user.is_staff = True
            user.is_superuser = True
            user.set_password(password)  # Force reset password every deploy
            user.save()
            
            if created:
                print(f"✅ Superuser '{username}' created successfully!")
            else:
                print(f"✅ Superuser '{username}' updated with fresh credentials!")
                
            print(f"📧 Email: {email}")
            print(f"🔗 Admin URL: /admin/")
            print(f"🎯 Password updated from Railway environment variables")
            
        except Exception as e:
            print(f"❌ Failed to create/update superuser: {e}")
