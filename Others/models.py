from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_date = models.DateField()

# Retrieving all books
books = Book.objects.all()

# Filtering books by author
books_by_author = Book.objects.filter(author='John Doe')

# Ordering books by published date
books_ordered = Book.objects.order_by('published_date')

# Creating a new book
new_book = Book(title='New Book', author='Jane Smith', published_date='2023-01-01')
new_book.save()