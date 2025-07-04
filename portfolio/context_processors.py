from .models import PersonalInfo, FooterLink

def portfolio_context(request):
    """Add portfolio-wide context variables"""
    # Get active personal info
    personal_info = PersonalInfo.get_active()
    
    # Get footer links grouped by category
    footer_links_by_category = {}
    for choice in FooterLink.LINK_CATEGORIES:
        category_key = choice[0]
        category_name = choice[1]
        links = FooterLink.objects.filter(
            category=category_key, 
            is_active=True
        ).order_by('order', 'title')
        if links.exists():
            footer_links_by_category[category_name] = links
    
    return {
        'personal_info': personal_info,
        'portfolio_name': personal_info.portfolio_name if personal_info else 'My Portfolio',
        'footer_links_by_category': footer_links_by_category,
    }
