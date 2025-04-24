from django.urls import path

from .views import getbooks, BookCreation, BookUpdate, BookLoan

urlpatterns = [
    path('', getbooks),
    path('new/', BookCreation.as_view()),
    path('update/<int:pk>/', BookUpdate.as_view()),
    path('loan/<int:pk>/', BookLoan.as_view()),
]