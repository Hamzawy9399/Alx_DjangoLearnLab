from rest_framework import generics, filters, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer
from django.shortcuts import get_object_or_404

class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'author__name']
    ordering_fields = ['publication_year', 'title']

class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save()

class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

class BookUpdateNoPKView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        pk = request.data.get('pk') or request.query_params.get('pk')
        if not pk:
            return Response({'detail': 'pk is required'}, status=status.HTTP_400_BAD_REQUEST)
        book = get_object_or_404(Book, pk=pk)
        serializer = BookSerializer(book, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        pk = request.data.get('pk') or request.query_params.get('pk')
        if not pk:
            return Response({'detail': 'pk is required'}, status=status.HTTP_400_BAD_REQUEST)
        book = get_object_or_404(Book, pk=pk)
        serializer = BookSerializer(book, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class BookDeleteNoPKView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        pk = request.data.get('pk') or request.query_params.get('pk')
        if not pk:
            return Response({'detail': 'pk is required'}, status=status.HTTP_400_BAD_REQUEST)
        book = get_object_or_404(Book, pk=pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request, *args, **kwargs):
        pk = request.data.get('pk') or request.query_params.get('pk')
        if not pk:
            return Response({'detail': 'pk is required'}, status=status.HTTP_400_BAD_REQUEST)
        book = get_object_or_404(Book, pk=pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
