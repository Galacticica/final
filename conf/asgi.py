"""
File: asgi.py
Author: Reagan Zierke
Date: 2025-04-27
Description: ASGI configuration for the Django project.
This file contains the ASGI application used by Django's development server and any ASGI-compatible web server.
"""



import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.settings')

application = get_asgi_application()
