# relationship_app/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views

# ✅ متطلبات تاسك 2
from .views import list_books
from .views import LibraryDetailView

# ✅ متطلبات تاسك 3 — لازم نضيف السطر ده
from . import views

app_name = 'relationship_app'

urlpatterns = [
    # ------------------------
    # Task 2: Function-based + Class-based views
    # ------------------------
    path('books/', list_books, name='list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),

    # ------------------------
    # Home page
    # ------------------------
    path('', list_books, name='home'),

    # ------------------------
    # Plain list view (debug/testing)
    # ------------------------
    path('books/plain/', views.list_books_plain, name='list_books_plain'),

    # ------------------------
    # Authentication URLs
    # ------------------------
    path('register/', views.register, name='register'),  # ✅ المطلوب من التاسك 3
    path('login/', auth_views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),

    # ------------------------
    # Role-based Access Control URLs
    # ------------------------
    path('role/admin/', views.admin_view, name='admin_view'),
    path('role/librarian/', views.librarian_view, name='librarian_view'),
    path('role/member/', views.member_view, name='member_view'),
]
