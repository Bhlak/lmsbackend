from django.db import models

class Book(models.Model):
    Title = models.CharField(max_length=120)
    Author = models.CharField(max_length=30)
    Publisher = models.CharField(max_length=40)
    Year_Published = models.DateTimeField()