"""
core/wsgi.py — WSGI entry for production (e.g. Gunicorn on Heroku).
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = get_wsgi_application()
