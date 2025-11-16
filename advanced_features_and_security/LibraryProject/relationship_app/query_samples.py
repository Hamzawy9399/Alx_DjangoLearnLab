# relationship_app/query_samples.py
from .models import Author, Book, Library, Librarian

def books_by_author(author_name):
    """Query all books by a specific author using filter()."""
    try:
        author = Author.objects.get(name=author_name)
    except Author.DoesNotExist:
        return []
    return list(Book.objects.filter(author=author))

def books_in_library(library_name):
    """List all books in a library by library name."""
    try:
        library = Library.objects.get(name=library_name)
    except Library.DoesNotExist:
        return []
    return list(library.books.all())

def librarian_for_library(library_name):
    """Retrieve the librarian for a library using Librarian.objects.get(library=...)."""
    try:
        library = Library.objects.get(name=library_name)
    except Library.DoesNotExist:
        return None

    try:
        librarian = Librarian.objects.get(library=library)
        return librarian
    except Librarian.DoesNotExist:
        return None

def run_all(sample_author='George Orwell', sample_library='Central Library'):
    """Run all queries as samples."""
    print('\n--- Running sample queries ---')

    print(f"\nBooks by author '{sample_author}':")
    for book in books_by_author(sample_author):
        print(' -', book.title)

    print(f"\nBooks in library '{sample_library}':")
    for book in books_in_library(sample_library):
        print(' -', book.title)

    librarian = librarian_for_library(sample_library)
    print(f"\nLibrarian for '{sample_library}': {librarian}")

    print('\n--- done ---')
