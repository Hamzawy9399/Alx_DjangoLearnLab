# relationship_app/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.detail import DetailView

from .models import Book, Library

def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

def register(request):
    """
    صفحة تسجيل مستخدم جديد باستخدام UserCreationForm.
    بعد التسجيل نقوم بعمل login آلي للمستخدم ونوجّهه إلى LOGIN_REDIRECT_URL.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # تسجيل دخول المستخدم فورًا
            login(request, user)
            return redirect('/')  # أو redirect(LOGIN_REDIRECT_URL)
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

# Optional plain view for quick debug (kept if you used it)
from django.http import HttpResponse
def list_books_plain(request):
    books = Book.objects.all()
    lines = [f"{b.title} by {b.author.name}" for b in books]
    return HttpResponse('<br>'.join(lines), content_type='text/html')

# Class-based view for Library detail (كما قبل)
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = self.object.books.all()
        return context
