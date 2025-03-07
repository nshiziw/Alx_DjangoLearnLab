# pip install djangorestframework
INSTALLED_APPS = [
    'rest_framework',
]

from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    published_date = models.DateField()


from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


from rest_framework import generics
from .models import MyModel
from .serializers import MyModelSerializer

class BookListCreateAPIView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


pythonCopy codefrom django.urls import path
from .views import BookListCreateAPIView

urlpatterns = [
    path("api/books", views.BookListCreateAPIView.as_view(), name="book_list_create"),
]
