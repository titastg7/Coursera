from .models import Book
from rest_framework import generics
from .serializers import BookSerializer

class BookView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class SingleBookView(generics.RetrieveUpdateAPIView) :
    queryset = Book.objects.all()
    serializer_class = BookSerializer