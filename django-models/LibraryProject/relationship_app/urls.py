# relationship_app/urls.py
from django.urls import path

from .views import list_books

from .views import LibraryDetailView

app_name = 'relationship_app'

urlpatterns = [
    # ✅ Function-based view: قائمة الكتب
    path('books/', list_books, name='list_books'),

    # ✅ Class-based view: تفاصيل مكتبة محددة
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
]
