"""
File: urls.py
Author: Reagan Zierke
Date: 2025-04-27
Description: URL configuration for the Adventure app.
"""



from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.GetAdventuresView.as_view(), name='get_adventures'),
    path('start/', views.StartAdventureView.as_view(), name='start_adventure'),
    path('status/', views.AdventureStatusView.as_view(), name='adventure_status'),
    path('complete/', views.CompleteAdventureView.as_view(), name='complete_adventure'),
]