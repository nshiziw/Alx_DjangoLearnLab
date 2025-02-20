from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')



from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()


from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)

class Course(models.Model):
    name = models.CharField(max_length=100)
    students = models.ManyToManyField(Student, related_name='courses')



from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')



from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

# Optimizing queries with prefetching
products = Product.objects.prefetch_related('category')













from django.http import HttpResponse

def hello_view(request):
    """A basic function view returning a greeting message."""
    return HttpResponse("Hello, World!")




from django.shortcuts import render
from .models import Book

def book_list(request):
      """Retrieves all books and renders a template displaying the list."""
      books = Book.objects.all()  # Fetch all book instances from the database
      context = {'book_list': books}  # Create a context dictionary with book list
      return render(request, 'books/book_list.html', context)






from django.views.generic import TemplateView

class HelloView(TemplateView):
    """A class-based view rendering a template named 'hello.html'."""
    template_name = 'hello.html'




from django.views.generic import DetailView
from .models import Book

class BookDetailView(DetailView):
  """A class-based view for displaying details of a specific book."""
  model = Book
  template_name = 'books/book_detail.html'

  def get_context_data(self, **kwargs):
    """Injects additional context data specific to the book."""
    context = super().get_context_data(**kwargs)  # Get default context data
    book = self.get_object()  # Retrieve the current book instance
    context['average_rating'] = book.get_average_rating() 









from django.views.generic import DetailView, UpdateView
from django.urls import reverse_lazy
from .models import Book

class BookUpdateView(UpdateView):
  """A class-based view for updating details of a specific book."""
  model = Book
  fields = ['title', 'author', 'description']  # Specify fields to be editable
  template_name = 'books/book_update_form.html'
  success_url = reverse_lazy('book_list')  # URL to redirect after successful update

  def form_valid(self, form):
    """Executes custom logic after form validation."""
    response = super().form_valid(form)  # Call default form validation
    # Perform additional actions after successful update (e.g., send notifications)
    return response
  











from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.hello_view, name='hello'),
    path('about/', views.AboutView.as_view(), name='about'),
]




<!-- book_list.html -->
<h1>Book List</h1>
<ul>
{% for book in book_list %}
  <li>{{ book.title }} by {{ book.author }}</li>
{% endfor %}
</ul>






<!-- base.html -->
<html>
  <head>
    <title>{% block title %}My Site{% endblock %}</title>
  </head>
  <body>
    {% block content %}{% endblock %}
  </body>
</html>

<!-- book_list.html -->
{% extends 'base.html' %}
{% block title %}Book List{% endblock %}
{% block content %}
  <h1>Book List</h1>
  <ul>
    {% for book in book_list %}
      <li>{{ book.title }} by {{ book.author }}</li>
    {% endfor %}
    </ul>
{% endblock %}








<a href="{% url 'book-detail' book.id %}">{{ book.title|truncatechars:30 }}</a>






<!-- base.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}My Site{% endblock %}</title>
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
</head>
<body>
    <!-- Content -->
    <script src="{% static 'js/script.js' %}"></script>
</body>
</html>