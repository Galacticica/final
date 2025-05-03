"""
File: urls.py
Author: Reagan Zierke
Date: 2025-04-27
Description: URL configuration for the Adventure app.
"""


from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('adventures/', include('adventures.urls')),
    path('gear/', include('gear.urls')),
]
