# relationship_app/admin.py
from django.contrib import admin
from django.apps import apps
from .models import Author, Book, Library, Librarian, UserProfile

# helper: register only if not already registered
def safe_register(model, admin_class=None):
    if model not in admin.site._registry:
        if admin_class:
            admin.site.register(model, admin_class)
        else:
            admin.site.register(model)

# Define admin classes
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author')
    list_filter = ('author',)

class LibraryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

class LibrarianAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'library')

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'role')
    search_fields = ('user__username', 'role')

# Use safe_register to avoid AlreadyRegistered errors
safe_register(Author, AuthorAdmin)
safe_register(Book, BookAdmin)
safe_register(Library, LibraryAdmin)
safe_register(Librarian, LibrarianAdmin)
safe_register(UserProfile, UserProfileAdmin)
