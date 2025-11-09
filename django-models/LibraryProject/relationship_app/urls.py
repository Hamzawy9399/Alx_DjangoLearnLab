# relationship_app/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views

from .views import list_books
from .views import LibraryDetailView
from . import views

app_name = 'relationship_app'

urlpatterns = [
    # Basic views
    path('', list_books, name='home'),
    path('books/', list_books, name='list_books'),
    path('books/plain/', views.list_books_plain, name='list_books_plain'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),

    # Book management (permission-protected)
    path('books/add/', views.add_book, name='add_book'),
    path('books/<int:pk>/edit/', views.edit_book, name='edit_book'),
    path('books/<int:pk>/delete/', views.delete_book, name='delete_book'),

    # Authentication
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),

    # Role-based
    path('role/admin/', views.admin_view, name='admin_view'),
    path('role/librarian/', views.librarian_view, name='librarian_view'),
    path('role/member/', views.member_view, name='member_view'),
]
