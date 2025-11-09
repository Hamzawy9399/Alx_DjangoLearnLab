# relationship_app/views.py
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from django.views.generic import DetailView

from .models import Book, Library

def list_books(request):

    books = Book.objects.select_related('author').all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

def list_books_plain(request):
    books = Book.objects.select_related('author').all()
    lines = [f"{b.title} by {b.author.name}" for b in books]
    return HttpResponse('<br>'.join(lines), content_type='text/html')


class LibraryDetailView(DetailView):


    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'


    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # جلب الكتب مختصراً (prefetch_related لتحسين الأداء مع ManyToMany)
        ctx['books'] = self.object.books.select_related('author').all()
        return ctx
# relationship_app/views.py (إضافة)
from django.shortcuts import render

def homepage(request):
    return render(request, 'relationship_app/index.html')
