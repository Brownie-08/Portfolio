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
    from whitenoise import WhiteNoise
    from django.conf.urls.static import static
    
    # Wrap the application with WhiteNoise to serve media files
    application = WhiteNoise(application)
    
    # Add media files to be served by WhiteNoise
    if hasattr(settings, 'MEDIA_ROOT') and settings.MEDIA_ROOT:
        application.add_files(str(settings.MEDIA_ROOT), prefix=settings.MEDIA_URL)
