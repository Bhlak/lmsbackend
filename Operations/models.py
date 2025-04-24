from django.db import models

from Signup.models import AppUser

class Book(models.Model):
    title = models.CharField(max_length=120)
    author = models.CharField(max_length=30)
    publisher = models.CharField(max_length=40)
    year_published = models.DateField()
    available = models.BooleanField(default=True)

class Loan(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrower = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    date_borrowed = models.DateField(auto_now_add=True)
    due_date = models.DateField()