# relationship_app/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views

from .views import list_books, list_books_plain, LibraryDetailView, register

app_name = 'relationship_app'

urlpatterns = [
    path('', list_books, name='home'),
    path('books/', list_books, name='list_books'),
    path('books/plain/', list_books_plain, name='list_books_plain'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),

    # Authentication URLs
    # Login (uses django.contrib.auth.views.LoginView)
    path('login/', auth_views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),

    # Logout (uses LogoutView) — template optional; we provide logout.html
    path('logout/', auth_views.LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),

    # Register (custom view)
    path('register/', register, name='register'),
]
