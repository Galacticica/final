"""
File: urls.py
Author: Reagan Zierke
Date: 2025-04-27
Description: URL configuration for the User app.
"""



from django.urls import path
from . import views
from . import admin_views

urlpatterns = [
    path('give_money/', admin_views.GiveMoneyView.as_view(), name='give_money'),
    path('give_xp/', admin_views.GiveXPView.as_view(), name='give_xp'),
    path('coinflip/', views.CoinFlipBetView.as_view(), name='coinflip_bet'),
    path('profile/', views.GetProfileView.as_view(), name='profile'),
    path('delete_user/', admin_views.DeleteUserView.as_view(), name='delete_user'),
    path('level_up/', views.LevelUpView.as_view(), name='level_up'),
]