"""
File: apps.py
Author: Reagan Zierke
Date: 2025-04-27
Description: Django app configuration for the Adventures app.
"""



from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
