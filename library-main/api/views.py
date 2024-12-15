from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Book, Transaction
from django.contrib.auth.models import User
from .serializers import BookSerializer, UserSerializer, TransactionSerializer
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # Filtering available books and search functionality
    def get_queryset(self):
        queryset = Book.objects.all()
        available = self.request.query_params.get('available')
        title = self.request.query_params.get('title')
        author = self.request.query_params.get('author')
        isbn = self.request.query_params.get('isbn')

        if available == 'true':
            queryset = queryset.filter(copies_available__gt=0)
        if title:
            queryset = queryset.filter(title__icontains=title) #  Case-Insensitive Searches
        if author:
            queryset = queryset.filter(author__icontains=author)
        if isbn:
            queryset = queryset.filter(isbn=isbn)
        return queryset

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class TransactionViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post']) # The @action  is used to define custom actions for a ViewSet. It allows you to add additional routes (endpoints) to the standard CRUD  by the ModelViewSet or ViewSet.
    def check_out(self, request):
        user = request.user
        book_id = request.data.get('book_id')
        if not book_id:
            return Response({'error': 'Book ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            book = Book.objects.get(id=book_id)
            if book.copies_available < 1:
                return Response({'error': 'No copies available'}, status=status.HTTP_400_BAD_REQUEST)
            # Check if user already has this book checked out
            if Transaction.objects.filter(user=user, book=book, returned_date__isnull=True).exists():
                return Response({'error': 'You have already checked out this book'}, status=status.HTTP_400_BAD_REQUEST)
            # Create transaction
            transaction = Transaction.objects.create(user=user, book=book)
            # Decrease available copies
            book.copies_available -= 1
            book.save()
            return Response(TransactionSerializer(transaction).data, status=status.HTTP_201_CREATED)
        except Book.DoesNotExist:
            return Response({'error': 'Book does not exist'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post']) # The @action(detail=False, methods=['get']) decorator in this context defines a custom action that allows the authenticated user to retrieve their borrowing history. This method provides a GET endpoint that returns all the Transaction instances associated with the logged-in user.
    def return_book(self, request):
        user = request.user
        book_id = request.data.get('book_id')
        if not book_id:
            return Response({'error': 'Book ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            transaction = Transaction.objects.get(user=user, book_id=book_id, returned_date__isnull=True)
            transaction.returned_date = timezone.now()
            transaction.save()
            # Increase available copies
            book = transaction.book
            book.copies_available += 1
            book.save()
            return Response(TransactionSerializer(transaction).data, status=status.HTTP_200_OK)
        except Transaction.DoesNotExist:
            return Response({'error': 'No checkout found for this book'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'])
    def my_borrowing_history(self, request):
        user = request.user
        transactions = Transaction.objects.filter(user=user)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)
