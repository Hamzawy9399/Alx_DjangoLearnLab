from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required, login_required
from django.views.decorators.http import require_http_methods
from django.utils.http import url_has_allowed_host_and_scheme
from django.conf import settings
from .models import Book
from .forms import BookForm

@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    q = request.GET.get('q', '').strip()
    if q:
        books = Book.objects.filter(title__icontains=q)
    else:
        books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books, 'query': q})

@permission_required('bookshelf.can_create', raise_exception=True)
@require_http_methods(["GET", "POST"])
def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            next_url = request.POST.get('next') or request.GET.get('next') or '/'
            if url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                return redirect(next_url)
            return redirect('bookshelf:book_list')
    else:
        form = BookForm()
    return render(request, 'bookshelf/form_example.html', {'form': form, 'action': 'create'})

@permission_required('bookshelf.can_edit', raise_exception=True)
@require_http_methods(["GET", "POST"])
def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            next_url = request.POST.get('next') or request.GET.get('next') or '/'
            if url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                return redirect(next_url)
            return redirect('bookshelf:book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'bookshelf/form_example.html', {'form': form, 'action': 'edit', 'book': book})

@permission_required('bookshelf.can_delete', raise_exception=True)
@require_http_methods(["GET", "POST"])
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('bookshelf:book_list')
    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})
