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
# أضف هذا في relationship_app/views.py

from django.http import HttpResponse

def list_books_plain(request):
    """
    بديل نصي بسيط لقائمة الكتب — يُستخدم إذا كان urls.py يشير إليه.
    يعرض عناوين الكتب مع أسماء المؤلفين مفصولة بأسطر <br>.
    """
    books = Book.objects.all()
    lines = [f"{b.title} by {b.author.name}" for b in books]
    # نستخدم content_type='text/html' عشان <br> يظهر في المتصفح
    return HttpResponse('<br>'.join(lines), content_type='text/html')
