from django.urls import path

from .views import UserRegistration

urlpatterns = [
    path('new/', UserRegistration.as_view())
]