# relationship_app/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views

# ✅ المطلوب حرفيًا في التاسك 2
from .views import list_books
from .views import LibraryDetailView

# باقي الاستيرادات للتاسكات التالية
from .views import (
    list_books_plain,
    register,
    admin_view,
    librarian_view,
    member_view,
)

app_name = 'relationship_app'

urlpatterns = [
    # ------------------------
    # Task 2: Function-based + Class-based views
    # ------------------------
    path('books/', list_books, name='list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),

    # ------------------------
    # Home (redirects to books)
    # ------------------------
    path('', list_books, name='home'),

    # ------------------------
    # Optional plain view (debug/testing)
    # ------------------------
    path('books/plain/', list_books_plain, name='list_books_plain'),

    # ------------------------
    # Authentication URLs
    # ------------------------
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),

    # ------------------------
    # Role-based Access Control URLs
    # ------------------------
    path('role/admin/', admin_view, name='admin_view'),
    path('role/librarian/', librarian_view, name='librarian_view'),
    path('role/member/', member_view, name='member_view'),
]
