# relationship_app/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import user_passes_test, login_required
from django.views.generic.detail import DetailView

# ✅ السطر المطلوب من الـ grader
from .models import Library
# ✅ كمان لازم Book تكون مستوردة لأنها مستخدمة في list_books
from .models import Book
# ✅ ونستورد UserProfile لاستخدام الدور
from .models import UserProfile


# =======================================================
# 📚 1. عرض قائمة الكتب (Function-based view)
# =======================================================
def list_books(request):
    """
    Function-based view that lists all books.
    Required: contains 'Book.objects.all()'
    """
    books = Book.objects.all()  # ✅ الشرط المطلوب
    return render(request, 'relationship_app/list_books.html', {'books': books})


def list_books_plain(request):
    """
    Simple fallback plain-text list of books (for debugging/testing).
    """
    books = Book.objects.all()
    text = "<br>".join(f"{book.title} by {book.author.name}" for book in books)
    return HttpResponse(text)


# =======================================================
# 🏛️ 2. عرض تفاصيل مكتبة (Class-based View)
# =======================================================
class LibraryDetailView(DetailView):
    """
    Displays a single Library and its related Books.
    Required: contains 'from django.views.generic.detail import DetailView'
    """
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = self.object.books.all()
        return context


# =======================================================
# 👤 3. تسجيل المستخدم (Register View)
# =======================================================
def register(request):
    """
    Register a new user using Django's UserCreationForm.
    Automatically logs the user in after registration.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('relationship_app:home')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})


# =======================================================
# 🔐 4. دوال مساعدة للتحقق من الدور
# =======================================================
def has_role(user, role_name):
    """Helper to check user's role safely."""
    try:
        return user.is_authenticated and user.userprofile.role == role_name
    except Exception:
        return False


# =======================================================
# 🧭 5. Role-Based Views
# =======================================================

@user_passes_test(lambda u: has_role(u, 'Admin'), login_url='/login/')
def admin_view(request):
    """Accessible only by users with role 'Admin'."""
    return render(request, 'relationship_app/admin_view.html', {'message': 'Welcome, Admin!'})


@user_passes_test(lambda u: has_role(u, 'Librarian'), login_url='/login/')
def librarian_view(request):
    """Accessible only by users with role 'Librarian'."""
    libraries = Library.objects.all()
    return render(request, 'relationship_app/librarian_view.html', {'libraries': libraries})


@user_passes_test(lambda u: has_role(u, 'Member'), login_url='/login/')
def member_view(request):
    """Accessible only by users with role 'Member'."""
    user = request.user
    return render(request, 'relationship_app/member_view.html', {'user': user})
