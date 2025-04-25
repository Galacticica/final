from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.GetAdventuresView.as_view(), name='get_adventures'),
]