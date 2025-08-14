from rest_framework import status, filters, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated

from .models import Book, Loan
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
    
class BookOps(APIView):
    permission_classes = ( IsAuthenticated, )
    
    def  get(self, request, pk):
        book = get_book(pk)
        return Response({"Message": "Book Retrieved Successfully", "Error": None}, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        book  = get_book(pk)
        serializer = BookSerializer(book, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"Message": "Book Updated Successfully", "Error": None}, status=status.HTTP_202_ACCEPTED)
        return Response({"Message": "Incorrect Parameters Provided", "Error": "Book Update Failed"}, status=status.HTTP_400_BAD_REQUEST)

class BookSearch(generics.ListCreateAPIView):
    search_fields = ['title', 'author', 'publisher', 'year_published']
    filter_backends = (filters.SearchFilter,)
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookLoan(APIView):
    permission_classes = ( IsAuthenticated, )

    def get_loan(self, pk):
        return Loan.objects.get(pk=pk)

    # Book Checkout = Loan Creation
    def post(self, request, pk):
        import datetime
        user = request.user

        book = get_book(pk)

        # Add 7 days to the date borrowed
        due_date = datetime.date.today() + datetime.timedelta(days=7)

        if (not Loan.objects.filter(book=book).exists()) and book.available:
            if user.loaned == 3:
                return Response({"Message": "User Cannot Borrow More Than Three Books At A Time", "Error": "Loan Creation Failed"}, status=status.HTTP_400_BAD_REQUEST)
            elif user.banned:
                return Response({"Message": "User Is Banned From The Library", "Error": "Loan Creation Failed"}, status=status.HTTP_400_BAD_REQUEST)
            
            data = dict()
            data['borrower'] = user.pk
            data['book'] = book.pk
            data['due_date'] = due_date

            serializer = LoanSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()

                user.loaned += 1
                user.save()

                book.available = False
                book.save()

                return Response({"Message": "Loan Created Successfully", "Data": serializer.data, "Error": None}, status=status.HTTP_201_CREATED)
            return Response({"Message": "Book Already Loaned Out", "Error": "Loan Creation Failed"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"Message": "Book Unavailable", "Error": "Loan Creation Failed"}, status=status.HTTP_400_BAD_REQUEST)

    # Book Return = Loan Deletion
    def delete(self, request, pk):
        loan = self.get_loan(pk)
        loan.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
