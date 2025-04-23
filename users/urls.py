from django.urls import path
from .views import GetOrCreateUserView

urlpatterns = [
    path('', GetOrCreateUserView.as_view(), name='get_or_create_user'),
]