"""
Custom storage configuration for serving media files in production.

This module provides a solution for serving media files on platforms like Render
that don't provide persistent file storage. For production applications, it's
recommended to use cloud storage services like AWS S3, Cloudinary, or similar.
"""

from whitenoise import WhiteNoise
from django.conf import settings
import os


class MediaWhiteNoise(WhiteNoise):
    """
    Custom WhiteNoise application that serves both static and media files.
    
    This is a temporary solution for development and testing purposes.
    For production applications, use dedicated cloud storage.
    """
    
    def __init__(self, application):
        super().__init__(application)
        
        # Add media files directory if it exists
        if hasattr(settings, 'MEDIA_ROOT') and settings.MEDIA_ROOT:
            media_root = str(settings.MEDIA_ROOT)
            if os.path.exists(media_root):
                self.add_files(media_root, prefix=settings.MEDIA_URL)


def configure_media_serving():
    """
    Configure media file serving for production environments.
    
    Returns:
        dict: Configuration for media file serving
    """
    if not settings.DEBUG:
        # In production, serve media files through the application
        # This is not ideal for high-traffic applications
        return {
            'WHITENOISE_USE_FINDERS': True,
            'WHITENOISE_AUTOREFRESH': True,
        }
    return {}
