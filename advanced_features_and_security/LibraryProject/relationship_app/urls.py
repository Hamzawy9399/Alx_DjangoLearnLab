# relationship_app/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views

# ✅ متطلبات التاسك 2
from .views import list_books
from .views import LibraryDetailView
# ✅ متطلبات التاسك 3
from . import views

app_name = 'relationship_app'

urlpatterns = [
    # ------------------------
    # Home + Books
    # ------------------------
    path('', list_books, name='home'),
    path('books/', list_books, name='list_books'),
    path('books/plain/', views.list_books_plain, name='list_books_plain'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),

    # ------------------------
    # ✅ Task 4: Permission-protected Book Management
    # ------------------------
    path('add_book/', views.add_book, name='add_book'),        # required literal
    path('edit_book/<int:pk>/', views.edit_book, name='edit_book'),  # required literal
    path('delete_book/<int:pk>/', views.delete_book, name='delete_book'),

    # ------------------------
    # Authentication
    # ------------------------
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),

    # ------------------------
    # Role-based Access
    # ------------------------
    path('role/admin/', views.admin_view, name='admin_view'),
    path('role/librarian/', views.librarian_view, name='librarian_view'),
    path('role/member/', views.member_view, name='member_view'),
]
