# relationship_app/urls.py
from django.urls import path
from .views import list_books
from .views import list_books_plain
from .views import LibraryDetailView

app_name = 'relationship_app'

urlpatterns = [
    path('', list_books, name='home'),                 # root -> books list
    path('books/', list_books, name='list_books'),
    path('books/plain/', list_books_plain, name='list_books_plain'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
]
