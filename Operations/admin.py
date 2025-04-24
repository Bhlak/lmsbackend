from django.contrib import admin
from .models import Book, Loan


@admin.register(Book)
class Book(admin.ModelAdmin):
    model = Book
    list_display = ('title', 'author')
    search_fields = ('title', 'author')

@admin.register(Loan)
class Loan(admin.ModelAdmin):
    model = Loan
    list_display = ('borrower', 'book', 'due_date')