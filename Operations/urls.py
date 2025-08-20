from django.urls import path

from .views import getbooks, BookCreation, BookOps, BookLoan, UserLoans, BookSearch

urlpatterns = [
    path('', getbooks),
    path('new/', BookCreation.as_view()),
    path('book/<int:pk>/', BookOps.as_view()),
    path('loan/<int:pk>/', BookLoan.as_view()),
    path('loans/', UserLoans.as_view()),
    path('search/', BookSearch.as_view()),
]