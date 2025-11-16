# relationship_app/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import permission_required, user_passes_test
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy

from django import forms

from .models import Library, Book, UserProfile


# --------------------
# BookForm (ModelForm)
# --------------------
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']


# --------------------
# Existing views (kept)
# --------------------
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})


def list_books_plain(request):
    books = Book.objects.all()
    text = "<br>".join(f"{book.title} by {book.author.name}" for book in books)
    return HttpResponse(text)


class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = self.object.books.all()
        return context


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('relationship_app:home')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})


def has_role(user, role_name):
    try:
        return user.is_authenticated and user.userprofile.role == role_name
    except Exception:
        return False


@user_passes_test(lambda u: has_role(u, 'Admin'), login_url='/login/')
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html', {'message': 'Welcome, Admin!'})


@user_passes_test(lambda u: has_role(u, 'Librarian'), login_url='/login/')
def librarian_view(request):
    libraries = Library.objects.all()
    return render(request, 'relationship_app/librarian_view.html', {'libraries': libraries})


@user_passes_test(lambda u: has_role(u, 'Member'), login_url='/login/')
def member_view(request):
    user = request.user
    return render(request, 'relationship_app/member_view.html', {'user': user})


# --------------------
# Permission-protected views for Book
# --------------------

@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    """
    Create a new Book. Requires 'relationship_app.can_add_book' permission.
    """
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('relationship_app:list_books')
    else:
        form = BookForm()
    return render(request, 'relationship_app/book_form.html', {'form': form, 'action': 'Add Book'})


@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, pk):
    """
    Edit an existing Book. Requires 'relationship_app.can_change_book' permission.
    """
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('relationship_app:list_books')
    else:
        form = BookForm(instance=book)
    return render(request, 'relationship_app/book_form.html', {'form': form, 'action': 'Edit Book', 'book': book})


@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, pk):
    """
    Delete a Book. Requires 'relationship_app.can_delete_book' permission.
    GET shows a confirmation template; POST performs the deletion.
    """
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('relationship_app:list_books')
    return render(request, 'relationship_app/book_confirm_delete.html', {'book': book})
