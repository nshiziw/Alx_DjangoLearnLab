from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from .models import Book, Author
from rest_framework.test import APITestCase

class BookApiTests(APITestCase):
    def setUp(self):
        # Create a test author
        self.author = Author.objects.create(name="Author Test")
        # Create a test book
        self.book = Book.objects.create(
            title="Test Book",
            publication_year=2023,
            author=self.author
        )
        # Create API client
        self.client = APIClient()
    
    def test_create_book(self):
        """Test creating a new book"""
        url = reverse('book-create')
        data = {
            'title': 'New Book',
            'publication_year': 2024,
            'author': self.author.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(Book.objects.get(id=2).title, 'New Book')
    
    def test_update_book(self):
        """Test updating an existing book"""
        url = reverse('book-update', args=[self.book.id])
        data = {
            'title': 'Updated Book',
            'publication_year': 2025,
            'author': self.author.id
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Book')
    
    def test_delete_book(self):
        """Test deleting a book"""
        url = reverse('book-delete', args=[self.book.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)
    
    def test_book_list(self):
        """Test retrieving the list of books"""
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_book_detail(self):
        """Test retrieving the detail of a single book"""
        url = reverse('book-detail', args=[self.book.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Book')
    
    def test_filter_books_by_title(self):
        """Test filtering books by title"""
        url = reverse('book-list') + '?title=Test Book'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_search_books_by_title(self):
        """Test searching books by title"""
        url = reverse('book-list') + '?search=Test'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_order_books_by_publication_year(self):
        """Test ordering books by publication year"""
        url = reverse('book-list') + '?ordering=publication_year'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'Test Book')
    
    def test_permissions_for_create_update_delete(self):
        """Test the permissions for creating, updating, and deleting books"""
        self.client.logout()
        # Test Create
        url = reverse('book-create')
        data = {'title': 'Book 2', 'publication_year': 2024, 'author': self.author.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Test Update
        url = reverse('book-update', args=[self.book.id])
        data = {'title': 'Book 2', 'publication_year': 2024, 'author': self.author.id}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Test Delete
        url = reverse('book-delete', args=[self.book.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Login as an authenticated user
        self.client.login(username='username', password='password')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
