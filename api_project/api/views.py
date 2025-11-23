from rest_framework import generics, viewsets
from .models import Book
from .serializers import BookSerializer
from .permissions import IsAdminForDeleteAuthenticatedForWriteOrReadOnly

class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by('id')
    serializer_class = BookSerializer
    permission_classes = [IsAdminForDeleteAuthenticatedForWriteOrReadOnly]
