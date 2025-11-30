from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from .models import Author, Book
from datetime import date, timedelta

class BookAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.author = Author.objects.create(name="Ahmed")
        self.book1 = Book.objects.create(title="Django Guide", publication_year=2020, author=self.author)
        self.book2 = Book.objects.create(title="Python Tricks", publication_year=2018, author=self.author)
        self.book3 = Book.objects.create(title="Advanced Django", publication_year=2021, author=self.author)

    def test_list_books_public(self):
        url = reverse("book-list")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIsInstance(resp.data, list)
        self.assertGreaterEqual(len(resp.data), 3)

    def test_search_and_ordering_and_filter(self):
        url = reverse("book-list")
        resp = self.client.get(url + "?search=Django")
        self.assertEqual(resp.status_code, 200)
        titles = [item["title"] for item in resp.data]
        self.assertIn("Django Guide", titles)
        self.assertIn("Advanced Django", titles)
        resp2 = self.client.get(url + "?ordering=-publication_year")
        self.assertEqual(resp2.status_code, 200)
        years = [item["publication_year"] for item in resp2.data]
        self.assertGreaterEqual(years[0], years[1])
        resp3 = self.client.get(url + "?author__name=Ahmed")
        self.assertEqual(resp3.status_code, 200)
        self.assertGreaterEqual(len(resp3.data), 3)

    def test_create_requires_auth_and_success(self):
        url = reverse("book-create")
        data = {"title": "New Book", "publication_year": 2019, "author": self.author.id}
        resp = self.client.post(url, data, format="json")
        self.assertIn(resp.status_code, (401, 403))
        self.client.force_authenticate(user=self.user)
        resp2 = self.client.post(url, data, format="json")
        self.assertEqual(resp2.status_code, 201)
        self.assertEqual(resp2.data["title"], "New Book")
        self.assertEqual(resp2.data["publication_year"], 2019)

    def test_publication_year_validation(self):
        url = reverse("book-create")
        future_year = date.today().year + 5
        data = {"title": "Future Book", "publication_year": future_year, "author": self.author.id}
        self.client.force_authenticate(user=self.user)
        resp = self.client.post(url, data, format="json")
        self.assertEqual(resp.status_code, 400)
        self.assertTrue("publication_year" in resp.data or any("publication_year" in str(v) for v in resp.data.values()))

    def test_update_by_pk_endpoint(self):
        url = reverse("book-update", args=[self.book1.pk])
        self.client.force_authenticate(user=self.user)
        resp = self.client.patch(url, {"title": "Django Guide Updated"}, format="json")
        self.assertEqual(resp.status_code, 200)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Django Guide Updated")

    def test_update_no_pk_endpoint(self):
        url = reverse("book-update-nopk")
        self.client.force_authenticate(user=self.user)
        resp = self.client.patch(url, {"pk": self.book2.pk, "title": "Python Tricks Updated"}, format="json")
        self.assertEqual(resp.status_code, 200)
        self.book2.refresh_from_db()
        self.assertEqual(self.book2.title, "Python Tricks Updated")

    def test_delete_by_pk_endpoint(self):
        url = reverse("book-delete", args=[self.book3.pk])
        self.client.force_authenticate(user=self.user)
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, 204)
        with self.assertRaises(Book.DoesNotExist):
            Book.objects.get(pk=self.book3.pk)

    def test_delete_no_pk_endpoint(self):
        book = Book.objects.create(title="ToDelete", publication_year=2017, author=self.author)
        url = reverse("book-delete-nopk")
        self.client.force_authenticate(user=self.user)
        resp = self.client.delete(url, {"pk": book.pk}, format="json")
        self.assertEqual(resp.status_code, 204)
        with self.assertRaises(Book.DoesNotExist):
            Book.objects.get(pk=book.pk)

    def test_permission_enforcement(self):
        create_url = reverse("book-create")
        self.client.logout()
        resp = self.client.post(create_url, {"title":"X", "publication_year":2010, "author": self.author.id}, format="json")
        self.assertIn(resp.status_code, (401, 403))
        detail_url = reverse("book-detail", args=[self.book1.pk])
        resp2 = self.client.get(detail_url)
        self.assertEqual(resp2.status_code, 200)
