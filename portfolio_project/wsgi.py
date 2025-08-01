"""
WSGI config for portfolio_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "portfolio_project.settings.prod")

application = get_wsgi_application()

# Add media file serving for production environments like Render
if not settings.DEBUG:
    try:
        from whitenoise import WhiteNoise
        import os
        
        # Wrap the application with WhiteNoise to serve media files
        application = WhiteNoise(application)
        
        # Add media files to be served by WhiteNoise
        if hasattr(settings, 'MEDIA_ROOT') and settings.MEDIA_ROOT:
            media_root = str(settings.MEDIA_ROOT)
            if os.path.exists(media_root):
                # Ensure the prefix doesn't have double slashes
                prefix = settings.MEDIA_URL.rstrip('/')
                application.add_files(media_root, prefix=prefix)
                print(f"WhiteNoise: Serving media files from {media_root} at {prefix}")
            else:
                print(f"Warning: Media root {media_root} does not exist")
        
        # Set some additional headers for media files
        application.max_age = 3600  # Cache media files for 1 hour
        
    except Exception as e:
        print(f"Warning: Could not configure WhiteNoise for media files: {e}")
