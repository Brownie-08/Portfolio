#!/usr/bin/env python
"""
Script to update Railway domain settings for CSRF and ALLOWED_HOSTS.
Run this after getting your actual Railway deployment domain.
"""

import os
from pathlib import Path

def update_railway_domain(domain):
    """Update the Railway settings file with the actual domain."""
    settings_file = Path(__file__).parent / 'portfolio_project' / 'settings' / 'railway.py'
    
    if not settings_file.exists():
        print(f"❌ Railway settings file not found: {settings_file}")
        return False
    
    # Read current content
    content = settings_file.read_text(encoding='utf-8')
    
    # Replace the CSRF_TRUSTED_ORIGINS section
    old_csrf_section = """# CSRF trusted origins for Railway
CSRF_TRUSTED_ORIGINS = []
if RAILWAY_DOMAIN:
    CSRF_TRUSTED_ORIGINS = [f'https://{RAILWAY_DOMAIN}']
else:
    # Common Railway domain patterns - update with your actual domain
    CSRF_TRUSTED_ORIGINS = [
        'https://portfolio-production-*.up.railway.app',
        'https://*.railway.app',
    ]"""
    
    new_csrf_section = f"""# CSRF trusted origins for Railway
CSRF_TRUSTED_ORIGINS = []
if RAILWAY_DOMAIN:
    CSRF_TRUSTED_ORIGINS = [f'https://{{RAILWAY_DOMAIN}}']
else:
    # Updated with actual Railway domain
    CSRF_TRUSTED_ORIGINS = [
        'https://{domain}',
        'https://*.railway.app',
    ]"""
    
    # Replace in content
    if old_csrf_section in content:
        content = content.replace(old_csrf_section, new_csrf_section)
        
        # Write back to file
        settings_file.write_text(content, encoding='utf-8')
        print(f"✅ Updated Railway domain to: {domain}")
        print("🚀 Ready to redeploy with proper CSRF configuration!")
        return True
    else:
        print("❌ Could not find CSRF section to update")
        return False

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python update_railway_domain.py your-app-name.up.railway.app")
        print("Example: python update_railway_domain.py portfolio-production-abc123.up.railway.app")
        sys.exit(1)
    
    domain = sys.argv[1]
    success = update_railway_domain(domain)
    sys.exit(0 if success else 1)
