from django.urls import path
from . import views

urlpatterns = [
    path('shop/', views.ShopListView.as_view(), name='shop'),
    path('gear_detail/', views.GearDetailView.as_view(), name='gear_detail'),
    path('purchase/', views.GearPurchaseView.as_view(), name='purchase'),
    path('owned_items/', views.OwnedGearView.as_view(), name='owned_items'),
    path('best_items/', views.BestGearView.as_view(), name='best_items'),
]