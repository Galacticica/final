"""
File: admin.py
Author: Reagan Zierke
Date: 2025-04-27
Description: Registers Adventure model with Django admin.
"""



from django.contrib import admin
from .models import Adventure

class AdventureAdmin(admin.ModelAdmin):
    list_display = ('name', 'required_level')

# Register your models here.
admin.site.register(Adventure, AdventureAdmin)