"""
Settings package for portfolio_project.

This package contains environment-specific settings.
The appropriate settings module is imported based on the DJANGO_SETTINGS_MODULE
environment variable or defaults to development settings.
"""
import os

# Determine which settings to use based on environment
ENVIRONMENT = os.environ.get('DJANGO_ENVIRONMENT', 'development')

if ENVIRONMENT == 'production':
    from .prod import *
elif ENVIRONMENT == 'deploy_check':
    from .deploy_check import *
elif ENVIRONMENT == 'development':
    from .dev import *
else:
    from .dev import *
