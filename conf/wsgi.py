"""
File: wsgi.py
Author: Reagan Zierke
Date: 2025-04-27
Description: WSGI configuration for the Django project.
This file contains the WSGI application used by Django's development server and any WSGI-compatible web server.
"""



import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.settings')

application = get_wsgi_application()
