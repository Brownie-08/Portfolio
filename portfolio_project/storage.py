"""
Custom storage configuration for serving media files in production.

This module provides a solution for serving media files on platforms like Render
that don't provide persistent file storage. For production applications, it's
recommended to use cloud storage services like AWS S3, Cloudinary, or similar.
"""

from whitenoise import WhiteNoise
from django.conf import settings
from django.core.files.storage import FileSystemStorage
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


class SelectiveCloudinaryStorage:
    """
    Custom storage that selectively uses Cloudinary for images while keeping other files local.
    This is used for resume files that need to stay local as per requirements.
    """
    
    def __init__(self, **settings_dict):
        self.cloudinary_storage = None
        self.local_storage = None
        self._init_storages()
    
    def _init_storages(self):
        """Initialize both storage backends"""
        # Initialize local storage
        self.local_storage = FileSystemStorage()
        
        # Initialize Cloudinary storage if available
        try:
            from cloudinary_storage.storage import MediaCloudinaryStorage
            self.cloudinary_storage = MediaCloudinaryStorage()
        except ImportError:
            self.cloudinary_storage = None
    
    def _should_use_local(self, name):
        """Determine if file should be stored locally"""
        # Keep resume/CV files local
        if ('resume' in name.lower() or 
            'cv' in name.lower() or 
            name.startswith('files/') or
            name.endswith('.pdf')):
            return True
        return False
    
    def _get_storage(self, name):
        """Get appropriate storage for the given file name"""
        if self._should_use_local(name) or not self.cloudinary_storage:
            return self.local_storage
        return self.cloudinary_storage
    
    def save(self, name, content, max_length=None):
        storage = self._get_storage(name)
        return storage.save(name, content, max_length)
    
    def delete(self, name):
        storage = self._get_storage(name)
        return storage.delete(name)
    
    def exists(self, name):
        storage = self._get_storage(name)
        return storage.exists(name)
    
    def url(self, name):
        storage = self._get_storage(name)
        return storage.url(name)
    
    def size(self, name):
        storage = self._get_storage(name)
        return storage.size(name)
    
    def open(self, name, mode='rb'):
        storage = self._get_storage(name)
        return storage.open(name, mode)


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
