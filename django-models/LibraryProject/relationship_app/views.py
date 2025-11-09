# relationship_app/views.py
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic.detail import DetailView

from .models import Library
from .models import Book

def list_books(request):
    """
    Function-based view that lists all books stored in the database.
    Uses Book.objects.all() as required.
    """
    books = Book.objects.all()
    # render template; هذا يمرر المتغير 'books' للقالب
    return render(request, 'relationship_app/list_books.html', {'books': books})

def list_books_plain(request):
    """
    Simple plain-text fallback (used only for quick debugging).
    """
    books = Book.objects.all()
    lines = [f"{b.title} by {b.author.name}" for b in books]
    return HttpResponse('<br>'.join(lines), content_type='text/html')

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = self.object.books.all()
        return context
