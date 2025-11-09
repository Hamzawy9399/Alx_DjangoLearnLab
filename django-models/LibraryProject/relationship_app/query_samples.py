# relationship_app/query_samples.py
import django
from django.core.exceptions import ObjectDoesNotExist

try:
    django.setup()
except Exception:
    pass

from .models import Author, Book, Library, Librarian

def books_by_author(author_name):
    """Query all books by a specific author name."""
    try:
        author = Author.objects.get(name=author_name)
    except Author.DoesNotExist:
        return []
    return list(author.books.all())

def books_in_library(library_name):
    """List all books in a library by library name."""
    try:
        library = Library.objects.get(name=library_name)
    except Library.DoesNotExist:
        return []
    # library.books هو ManyToMany
    return list(library.books.all())

def librarian_for_library(library_name):
    """Retrieve the librarian for a library by name."""
    try:
        library = Library.objects.get(name=library_name)
    except Library.DoesNotExist:
        return None
    return getattr(library, 'librarian', None)

def run_all(sample_author='George Orwell', sample_library='Central Library'):
    print('\\n--- Running sample queries ---')
    print(f"Books by author '{sample_author}':")
    books = books_by_author(sample_author)
    if not books:
        print("  (no books found)")
    for b in books:
        print(' -', b.title)

    print(f"\\nBooks in library '{sample_library}':")
    books = books_in_library(sample_library)
    if not books:
        print("  (no books found)")
    for b in books:
        print(' -', b.title)

    lib_librarian = librarian_for_library(sample_library)
    print(f"\\nLibrarian for '{sample_library}': {lib_librarian}")
    print('--- done ---\\n')
