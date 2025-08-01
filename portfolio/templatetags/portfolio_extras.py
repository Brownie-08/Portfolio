from django import template
from django.urls import reverse
from django.conf import settings

register = template.Library()

@register.filter
def split_skills(value, category=None):
    """Split comma-separated skills into a list"""
    if not value:
        return []
    return [skill.strip() for skill in value.split(',') if skill.strip()]

@register.filter
def split_by_comma(value):
    """Split comma-separated values into a list"""
    if not value:
        return []
    return [item.strip() for item in value.split(',') if item.strip()]

@register.filter
def get_whatsapp_link(phone_number):
    """Convert phone number to WhatsApp link"""
    if not phone_number:
        return ''
    # Remove non-digit characters
    clean_number = ''.join(filter(str.isdigit, phone_number))
    return f'https://wa.me/{clean_number}'

@register.simple_tag
def get_skills_by_category(skills, category):
    """Get skills filtered by category"""
    return skills.filter(category=category).order_by('order', 'name')

@register.filter
def split(value, delimiter=','):
    """
    Split a string by delimiter and return a list
    Usage: {{ "python,javascript,react"|split:"," }}
    """
    if value:
        return [item.strip() for item in value.split(delimiter) if item.strip()]
    return []

@register.filter
def trim(value):
    """
    Trim whitespace from a string
    Usage: {{ " hello world "|trim }}
    """
    if value:
        return value.strip()
    return value

@register.filter
def tech_stack_list(tech_stack):
    """
    Convert tech_stack string to list
    Usage: {{ project.tech_stack|tech_stack_list }}
    """
    if tech_stack:
        return [tech.strip() for tech in tech_stack.split(',') if tech.strip()]
    return []

@register.filter
def mul(value, arg):
    """
    Multiply two values
    Usage: {{ value|mul:20 }}
    """
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def media_url_fallback(file_field):
    """
    Generate a fallback media URL for production environments.
    If the direct media URL doesn't work, use the fallback view.
    
    Usage: {{ personal_info.profile_image|media_url_fallback }}
    """
    if not file_field:
        return ''
    
    try:
        # Check if file exists and has a name
        if not hasattr(file_field, 'name') or not file_field.name:
            return ''
        
        # Get the URL from the file field
        url = file_field.url
        
        # Debug: Print URL to console (remove in production)
        print(f"Debug - File URL: {url}")
        
        # Return the URL as-is since Cloudinary handles URL generation
        return url
        
    except (ValueError, AttributeError, Exception) as e:
        print(f"Error getting media URL: {e}")
        # If direct URL fails, try the fallback view
        try:
            if hasattr(file_field, 'name') and file_field.name:
                return reverse('portfolio:serve_media', kwargs={'path': file_field.name})
        except Exception as fallback_error:
            print(f"Fallback URL generation failed: {fallback_error}")
            pass
        return ''

@register.simple_tag
def profile_image_url(personal_info):
    """
    Get the profile image URL with production fallback.
    
    Usage: {% profile_image_url personal_info %}
    """
    if not personal_info or not personal_info.profile_image:
        return None
    
    try:
        # Try to get the direct media URL first
        url = personal_info.profile_image.url
        # Ensure the URL is properly formatted
        if url and not url.startswith('http'):
            from django.conf import settings
            if hasattr(settings, 'MEDIA_URL'):
                if not url.startswith(settings.MEDIA_URL):
                    url = settings.MEDIA_URL + url.lstrip('/')
        return url
    except (ValueError, AttributeError, Exception):
        # Fallback to the serve view
        try:
            return reverse('portfolio:serve_profile_image')
        except:
            return None

@register.simple_tag
def resume_download_url(personal_info):
    """
    Get the resume download URL with production fallback.
    
    Usage: {% resume_download_url personal_info %}
    """
    if not personal_info or not personal_info.resume:
        return ''
    
    try:
        return personal_info.resume.url
    except (ValueError, AttributeError):
        return reverse('portfolio:serve_resume')

@register.filter
def file_exists(file_field):
    """
    Check if a file field's file actually exists.
    
    Usage: {{ personal_info.profile_image|file_exists }}
    """
    if not file_field:
        return False
    
    try:
        import os
        from django.conf import settings
        
        if hasattr(file_field, 'path'):
            return os.path.exists(file_field.path)
        elif hasattr(file_field, 'name') and file_field.name:
            file_path = os.path.join(settings.MEDIA_ROOT, file_field.name)
            return os.path.exists(file_path)
        return False
    except (ValueError, AttributeError, OSError):
        return False
