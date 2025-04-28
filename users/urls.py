"""
File: urls.py
Author: Reagan Zierke
Date: 2025-04-27
Description: URL configuration for the User app.
"""



from django.urls import path
from . import views

urlpatterns = [
    path('', views.GetOrCreateUserView.as_view(), name='get_or_create_user'),
    path('give_money/', views.GiveMoneyView.as_view(), name='give_money'),
    path('coinflip/', views.CoinFlipBetView.as_view(), name='coinflip_bet'),
    path('profile/', views.GetOrCreateUserView.as_view(), name='profile'),
    path('delete_user/', views.DeleteUserView.as_view(), name='delete_user'),
    path('level_up/', views.LevelUpView.as_view(), name='level_up'),
]