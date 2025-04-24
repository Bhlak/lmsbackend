from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated

from .models import Book
from .serializers import BookSerializer, LoanSerializer


@api_view(['GET'])
def getbooks(request):
    queryset = Book.objects.all()
    books = BookSerializer(queryset, many=True)
    return Response({"Message": "Books Retrieved", "Data": books.data, "Error": None}, status=status.HTTP_200_OK)

def get_book(pk):
    return Book.objects.get(pk=pk)

class BookCreation(APIView):
    permission_classes = ( IsAuthenticated, )


    def post(self, request):
        title = request.data['title']

        unwanted = request.data.pop('available', None)

        if not Book.objects.filter(title__exact=title).exists():
            serializer = BookSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                book = serializer.save()

                return Response({"Message": "Book Created Successfully", "Error": None, "Data": serializer.data}, status=status.HTTP_201_CREATED)


        return Response({"Message": "A Book With That Title Already Exists", "Error": "Book Creation Failed"}, status=status.HTTP_400_BAD_REQUEST)
    
class BookUpdate(APIView):
    permission_classes = ( IsAuthenticated, )

    def patch(self, request, pk):
        book  = get_object(pk)
        serializer = BookSerializer(book, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"Message": "Book Updated Successfully", "Error": None}, status=status.HTTP_202_ACCEPTED)
        return Response({"Message": "Incorrect Parameters Provided", "Error": "Book Update Failed"}, status=status.HTTP_400_BAD_REQUEST)

class BookLoan(APIView):
    permission_classes = ( IsAuthenticated, )

    def post(self, request, pk):
        import datetime
        user = request.user

        book = get_book(pk)

        # Add 7 days to the date borrowed
        due_date = datetime.date.today() + datetime.timedelta(days=7)

        data = dict()
        data['borrower'] = user.pk
        data['book'] = book.pk
        data['due_date'] = due_date

        serializer = LoanSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            

            return Response({"Message": "Loan Created Successfully", "Data": serializer.data, "Error": None}, status=status.HTTP_201_CREATED)
        return Response({"Message": "Incorrect Parameters Provided For Loan", "Error": "Loan Creation Failed"}, status=status.HTTP_400_BAD_REQUEST)

        
