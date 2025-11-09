# relationship_app/views.py
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse


from django.views.generic.detail import DetailView


from .models import Library
from .models import Book


# ---------------------------
# Function-based View
# ---------------------------
def list_books(request):
    """
    Function-based view that lists all books stored in the database.
    Displays each book title and its author.
    """

    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})


# ---------------------------
# Class-based View
# ---------------------------
class LibraryDetailView(DetailView):
    """
    Class-based view showing details for a specific library and its books.
    """
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['books'] = self.object.books.all()
        return context
