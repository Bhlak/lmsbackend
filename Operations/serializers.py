from rest_framework import serializers
from .models import Book, Loan

class BookSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True)
    author = serializers.CharField(required=True)
    publisher = serializers.CharField(required=True)
    year_published = serializers.CharField(required=True)
    pk = serializers.CharField(read_only=True)

    class Meta:
        model = Book
        fields = "__all__"
    
    def create(self, data):
        book = Book.objects.create(**data)

        if book:
            return book
        return None
    
class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = "__all__"

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        
        rep['book'] = instance.book.title

        return rep 