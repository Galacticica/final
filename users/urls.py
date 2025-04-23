from django.urls import path
from .views import GetOrCreateUserView, CoinFlipBetView, GiveMoneyView

urlpatterns = [
    path('', GetOrCreateUserView.as_view(), name='get_or_create_user'),
    path('give_money/', GiveMoneyView.as_view(), name='give_money'),
    path('coinflip/', CoinFlipBetView.as_view(), name='coinflip_bet'),
]