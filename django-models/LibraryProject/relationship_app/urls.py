# relationship_app/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views  # ✅ لازم السطر ده موجود حرفيًا

app_name = 'relationship_app'

urlpatterns = [
    # الصفحات الأساسية
    path('', views.list_books, name='home'),
    path('books/', views.list_books, name='list_books'),
    path('books/plain/', views.list_books_plain, name='list_books_plain'),
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),

    # ✅ التسجيل باستخدام views.register (ده المطلوب)
    path('register/', views.register, name='register'),

    # ✅ تسجيل الدخول والخروج باستخدام Django built-in
    path('login/', auth_views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
]
