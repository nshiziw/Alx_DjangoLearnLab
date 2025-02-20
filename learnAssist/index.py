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








from django.contrib.auth.models import User

# Create a new user
user = User.objects.create_user('john', 'john@example.com', 'password123')

# Retrieve a user based on username
user = User.objects.get(username='john')







from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'










from django.contrib.auth.views import LoginView
from django.urls import path

urlpatterns = [
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
]







from django.contrib.auth.views import LogoutView
from django.urls import path

urlpatterns = [
    path('logout/', LogoutView.as_view(), name='logout'),
]








from django.contrib.auth.decorators import login_required

@login_required
def profile_view(request):
    # This view can only be accessed by authenticated users
    return render(request, 'profile.html')








# settings.py
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 9,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]





pythonCopy codefrom django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

urlpatterns = [
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]





pythonCopy codefrom django.contrib.auth import views as auth_views
from django.urls import path

urlpatterns = [
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]





pythonCopy codefrom django.contrib.auth import views as auth_views
from django.urls import path

urlpatterns = [
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
]









INSTALLED_APPS = [
    ...
    'django.contrib.auth',
    'django.contrib.contenttypes',
    ...
]




MIDDLEWARE = [
        ...,
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    ...
]




from django.urls import path, include

urlpatterns = [
    ...,

    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/',
             TemplateView.as_view(template_name='accounts/profile.html'),
             name='profile'),
    path("signup/", SignUpView.as_view(), name="templates/registration/signup"),
        ...
]




LOGIN_REDIRECT_URL = "/accounts/profile"
LOGOUT_REDIRECT_URL = "/accounts/profile"




TEMPLATES = [
    {
        ...
        'DIRS': [ BASE_DIR / "templates" ],
          ...
    },
]








from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
