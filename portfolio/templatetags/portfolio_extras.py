from django import template

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
