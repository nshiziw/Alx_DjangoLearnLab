from rest_framework import serializers
from .models import BlogPost, Comment

class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'author', 'author_name', 'created_at']




from rest_framework import serializers
from .models import BlogPost

class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'content', 'author', 'created_at']

    def validate(self, data):
        if len(data['title']) < 5:
            raise serializers.ValidationError("Title must be at least 5 characters long.")
        return data





from rest_framework import serializers
from .models import BlogPost, Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'author', 'created_at']

class BlogPostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'content', 'author', 'comments', 'created_at']





from rest_framework import generics
from .models import Book #replace with your working model
from .serializers import BookSerializer # replace with your project's serializer

class CustomBookCreateView(generics.CreateAPIView):
# can be any name, ensure to align with your project as this is sample exampls 
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class CustomBookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer





from django.contrib.auth.mixins import LoginRequiredMixin
class MyView(LoginRequiredMixin, View):
   login_url = '/login/'
   redirect_field_name = 'redirect_to'

   def get(self, request):
       # Your view logic here


return Users.objects.filter(role=Teachers)


from myapp.models import Purchase
from myapp.serializers import PurchaseSerializer
from rest_framework import generics

class PurchaseList(generics.ListAPIView):
    serializer_class = PurchaseSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        return Purchase.objects.filter(purchaser=user)
    re_path('^purchases/(?P<username>.+)/$', PurchaseList.as_view()),





class PurchaseList(generics.ListAPIView):
    serializer_class = PurchaseSerializer

    def get_queryset(self):
        """
        This view returns a list of purchases for the user specified in the URL.
        """
        username = self.kwargs['username']
        return Purchase.objects.filter(purchaser__username=username)
    




class PurchaseList(generics.ListAPIView):
    serializer_class = PurchaseSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a specific user,
        by filtering based on the `username` query parameter in the URL.
        """
        queryset = Purchase.objects.all()
        username = self.request.query_params.get('username')
        if username is not None:
            queryset = queryset.filter(purchaser__username=username)
        return queryset
    





from rest_framework import filters

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email']





class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['username', 'email']





from rest_framework.test import APIRequestFactory

 Using the standard RequestFactory API to create a form POST request
factory = APIRequestFactory()
request = factory.post('/notes/', {'title': 'new idea'})





from django.test import TestCase
from myapp.models import Animal


class AnimalTestCase(TestCase):
    def setUp(self):
        Animal.objects.create(name="lion", sound="roar")
        Animal.objects.create(name="cat", sound="meow")

    def test_animals_can_speak(self):
        """Animals that can speak are correctly identified"""
        lion = Animal.objects.get(name="lion")
        cat = Animal.objects.get(name="cat")
        self.assertEqual(lion.speak(), 'The lion says "roar"')
        self.assertEqual(cat.speak(), 'The cat says "meow"')





