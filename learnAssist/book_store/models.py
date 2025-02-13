from django.db import models

# Create your models here.

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

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

# from myapp.models import Product

product = Product.objects.create(
    name="Laptop",
    description="High-performance laptop",
    price=1200.99,
    category="Electronics"
)


products = Product.objects.all()
for product in products:
    print(product.name, product.price)

product = Product.objects.get(id=1)
print(product.name)

product = Product.objects.get(id=1)
product.price = 1100.50
product.save()

product = Product.objects.get(id=1)
product.delete()


electronics = Product.objects.filter(category="Electronics")

products_by_price = Product.objects.order_by('price')

products_by_price_desc = Product.objects.order_by('-price')
