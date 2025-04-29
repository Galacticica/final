"""
File: urls.py
Author: Reagan Zierke
Date: 2025-04-27
Description: URL configuration for the User app.
"""



from django.urls import path
from . import views_user
from . import views_admin
from . import views_gamble

urlpatterns = [
    path('give_money/', views_admin.GiveMoneyView.as_view(), name='give_money'),
    path('give_xp/', views_admin.GiveXPView.as_view(), name='give_xp'),
    path('coinflip/', views_gamble.CoinFlipBetView.as_view(), name='coinflip_bet'),
    path('profile/', views_user.GetProfileView.as_view(), name='profile'),
    path('delete_user/', views_admin.DeleteUserView.as_view(), name='delete_user'),
    path('level_up/', views_user.LevelUpView.as_view(), name='level_up'),
]