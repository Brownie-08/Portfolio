"""
Custom model fields for handling selective storage between Cloudinary and local storage
"""
from django.db import models
from django.core.files.storage import default_storage
from django.conf import settings


class SelectiveFileField(models.FileField):
    """
    Custom FileField that uses local storage for resume files and Cloudinary for others
    Also handles already migrated Cloudinary URLs correctly
    """
    
    def __init__(self, *args, **kwargs):
        self.force_local = kwargs.pop('force_local', False)
        super().__init__(*args, **kwargs)
    
    def pre_save(self, model_instance, add):
        """Handle file saving with selective storage"""
        file = super().pre_save(model_instance, add)
        
        # If it's already a Cloudinary URL, leave it alone
        if file and isinstance(file.name, str) and 'cloudinary.com' in file.name:
            return file
            
        # If force_local is True (for resume fields), ensure local storage
        if self.force_local and file:
            # Set storage to local for this field
            from django.core.files.storage import FileSystemStorage
            file.storage = FileSystemStorage()
        
        return file


class ResumeFileField(SelectiveFileField):
    """Specialized field for resume files that always uses local storage"""
    
    def __init__(self, *args, **kwargs):
        kwargs['force_local'] = True
        super().__init__(*args, **kwargs)
