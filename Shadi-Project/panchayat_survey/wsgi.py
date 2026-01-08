"""
WSGI config for panchayat_survey project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'panchayat_survey.settings')

application = get_wsgi_application()

