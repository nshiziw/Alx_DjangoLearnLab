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




from rest_framework import serializers
from .models import MyModel

class MyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyModel
        fields = ['id', 'name', 'description', 'created_at']



from rest_framework import serializers
from .models import MyModel

class MyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyModel
        fields = ['id', 'name', 'description', 'created_at']

    def validate(self, data):
        if len(data['name']) < 5:
            raise serializers.ValidationError("Name must be at least 5 characters long.")
        return data



from rest_framework import serializers
from .models import MyModel

class MyModelSerializer(serializers.ModelSerializer):
    days_since_created = serializers.SerializerMethodField()

    class Meta:
        model = MyModel
        fields = ['id', 'name', 'description', 'created_at', 'days_since_created']

    def get_days_since_created(self, obj):
        from datetime import datetime, timezone
        return (datetime.now(timezone.utc) - obj.created_at).days
    



from rest_framework import generics
from .models import MyModel
from .serializers import MyModelSerializer

class MyModelListCreateAPIView(generics.ListCreateAPIView):
    queryset = MyModel.objects.all()
    serializer_class = MyModelSerializer

    def get_queryset(self):
        queryset = self.queryset
        name_filter = self.request.query_params.get('name', None)
        if name_filter is not None:
            queryset = queryset.filter(name__icontains=name_filter)
        return queryset