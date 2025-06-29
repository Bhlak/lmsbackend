from django.urls import path
from . import views
from .views import LoginView, LogoutView, Test, GetUserDetails

urlpatterns = [
    path('', views.getUsers),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('test/', Test.as_view()),
    path('user/', GetUserDetails.as_view()),
]