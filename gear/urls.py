from django.urls import path
from . import views

urlpatterns = [
    path('shop/', views.ShopListView.as_view(), name='shop'),
    path('gear_detail/', views.GearDetailView.as_view(), name='gear_detail'),
]