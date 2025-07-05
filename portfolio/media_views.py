"""
Media file serving views for production environments.

This module provides fallback views for serving media files when
the primary serving mechanism (WhiteNoise) doesn't work as expected.
"""

import os
import mimetypes
from django.http import HttpResponse, Http404, FileResponse
from django.conf import settings
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_GET


@require_GET
@cache_control(max_age=3600)  # Cache for 1 hour
def serve_media(request, path):
    """
    Serve media files in production.
    
    This view serves media files when the standard Django development
    server media serving is not available in production.
    
    Args:
        request: The HTTP request object
        path: The relative path to the media file
        
    Returns:
        FileResponse: The media file response
        
    Raises:
        Http404: If the file is not found
    """
    # Construct the full file path
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    
    # Security check: ensure the file is within MEDIA_ROOT
    media_root = os.path.abspath(settings.MEDIA_ROOT)
    file_path = os.path.abspath(file_path)
    
    if not file_path.startswith(media_root):
        raise Http404("File not found")
    
    # Check if file exists
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        raise Http404("File not found")
    
    # Determine content type
    content_type, _ = mimetypes.guess_type(file_path)
    if content_type is None:
        content_type = 'application/octet-stream'
    
    # Return the file
    try:
        return FileResponse(
            open(file_path, 'rb'),
            content_type=content_type,
            as_attachment=False
        )
    except IOError:
        raise Http404("File not found")


@require_GET
def serve_profile_image(request):
    """
    Serve the current user's profile image.
    
    This is a convenience view for serving the active user's profile image.
    """
    from .models import PersonalInfo
    
    try:
        personal_info = PersonalInfo.get_active()
        if personal_info and personal_info.profile_image:
            file_path = personal_info.profile_image.path
            if os.path.exists(file_path):
                content_type, _ = mimetypes.guess_type(file_path)
                if content_type is None:
                    content_type = 'image/jpeg'
                
                return FileResponse(
                    open(file_path, 'rb'),
                    content_type=content_type,
                    as_attachment=False
                )
    except Exception:
        pass
    
    raise Http404("Profile image not found")


@require_GET
def serve_resume(request):
    """
    Serve the current user's resume/CV file.
    
    This is a convenience view for serving the active user's resume.
    """
    from .models import PersonalInfo
    
    try:
        personal_info = PersonalInfo.get_active()
        if personal_info and personal_info.resume:
            file_path = personal_info.resume.path
            if os.path.exists(file_path):
                content_type, _ = mimetypes.guess_type(file_path)
                if content_type is None:
                    content_type = 'application/pdf'
                
                # Get the original filename for download
                filename = os.path.basename(personal_info.resume.name)
                
                response = FileResponse(
                    open(file_path, 'rb'),
                    content_type=content_type,
                    as_attachment=True,
                    filename=filename
                )
                return response
    except Exception:
        pass
    
    raise Http404("Resume not found")
