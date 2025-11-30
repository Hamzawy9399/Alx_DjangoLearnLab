from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Author, Book
from datetime import date

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
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertGreaterEqual(len(response.data), 3)

    def test_search_and_order_and_filter(self):
        url = reverse("book-list")
        response = self.client.get(url + "?search=Django")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [item["title"] for item in response.data]
        self.assertIn("Django Guide", titles)
        self.assertIn("Advanced Django", titles)

        response2 = self.client.get(url + "?ordering=-publication_year")
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        years = [item["publication_year"] for item in response2.data]
        self.assertGreaterEqual(years[0], years[1])

        response3 = self.client.get(url + "?author__name=Ahmed")
        self.assertEqual(response3.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response3.data), 3)

    def test_create_requires_auth_and_success(self):
        url = reverse("book-create")
        data = {"title": "New Book", "publication_year": 2019, "author": self.author.id}
        response = self.client.post(url, data, format="json")
        self.assertIn(response.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

        self.client.force_authenticate(user=self.user)
        response2 = self.client.post(url, data, format="json")
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.data["title"], "New Book")

    def test_publication_year_validation(self):
        url = reverse("book-create")
        future_year = date.today().year + 5
        data = {"title": "Future Book", "publication_year": future_year, "author": self.author.id}
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue("publication_year" in str(response.data))

    def test_update_by_pk(self):
        url = reverse("book-update", args=[self.book1.pk])
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, {"title": "Django Updated"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Django Updated")

    def test_update_no_pk(self):
        url = reverse("book-update-nopk")
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, {"pk": self.book2.pk, "title": "Python Updated"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book2.refresh_from_db()
        self.assertEqual(self.book2.title, "Python Updated")

    def test_delete_by_pk(self):
        url = reverse("book-delete", args=[self.book3.pk])
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Book.DoesNotExist):
            Book.objects.get(pk=self.book3.pk)

    def test_delete_no_pk(self):
        book = Book.objects.create(title="Temp Delete", publication_year=2017, author=self.author)
        url = reverse("book-delete-nopk")
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url, {"pk": book.pk}, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Book.DoesNotExist):
            Book.objects.get(pk=book.pk)

    def test_permission_rules(self):
        create_url = reverse("book-create")
        response = self.client.post(create_url, {"title": "X", "publication_year": 2010, "author": self.author.id}, format="json")
        self.assertIn(response.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

        detail_url = reverse("book-detail", args=[self.book1.pk])
        response2 = self.client.get(detail_url)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
