"""
File: admin.py
Author: Reagan Zierke
Date: 2025-04-27
Description: Registers Adventure model with Django admin.
"""



from django.contrib import admin
from .models import Adventure


# Register your models here.
admin.site.register(Adventure)