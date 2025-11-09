# relationship_app/models.py
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save

User = get_user_model()


# ============================================================
# 1️⃣ Author Model
# ============================================================
class Author(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# ============================================================
# 2️⃣ Book Model
# ============================================================
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    publication_year = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.title


# ============================================================
# 3️⃣ Library Model
# ============================================================
class Library(models.Model):
    name = models.CharField(max_length=255)
    # ✅ نستخدم موديل وسيط مخصص لحل خطأ E336
    books = models.ManyToManyField(Book, through='LibraryBooks', related_name='libraries', blank=True)

    def __str__(self):
        return self.name


# ============================================================
# 4️⃣ LibraryBooks (through model)
# ============================================================
class LibraryBooks(models.Model):
    library = models.ForeignKey(Library, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('library', 'book')
        verbose_name = "Library Book"
        verbose_name_plural = "Library Books"

    def __str__(self):
        return f"{self.library.name} — {self.book.title}"


# ============================================================
# 5️⃣ Librarian Model
# ============================================================
class Librarian(models.Model):
    name = models.CharField(max_length=255)
    library = models.OneToOneField(Library, on_delete=models.CASCADE, related_name='librarian')

    def __str__(self):
        return f"{self.name} ({self.library.name})"


# ============================================================
# 6️⃣ UserProfile Model — Role-based extension of User
# ============================================================
class UserProfile(models.Model):
    ROLE_ADMIN = 'Admin'
    ROLE_LIBRARIAN = 'Librarian'
    ROLE_MEMBER = 'Member'
    ROLE_CHOICES = [
        (ROLE_ADMIN, 'Admin'),
        (ROLE_LIBRARIAN, 'Librarian'),
        (ROLE_MEMBER, 'Member'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='userprofile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_MEMBER)

    def __str__(self):
        return f"{self.user.username} - {self.role}"


# ============================================================
# 7️⃣ Signal to auto-create UserProfile after User creation
# ============================================================
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
