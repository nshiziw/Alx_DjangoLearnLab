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
    


from rest_framework import viewsets
from .models import MyModel
from .serializers import MyModelSerializer

class MyModelViewSet(viewsets.ModelViewSet):
    queryset = MyModel.objects.all()
    serializer_class = MyModelSerializer



from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MyModelViewSet

router = DefaultRouter()
router.register(r'my-models', MyModelViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]



from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MyModelViewSet, AnotherModelViewSet

router = DefaultRouter()
router.register(r'my-models', MyModelViewSet)
router.register(r'another-models', AnotherModelViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    # Add any additional non-viewset-based endpoints here
]



from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

class MyAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Only authenticated users can access this view
        return Response({'message': 'Hello, authenticated user!'})




from rest_framework.permissions import BasePermission

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return request.user.is_staff



from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView

class MyModelListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Only authenticated users can view the list of models
        queryset = MyModel.objects.all()
        serializer = MyModelSerializer(queryset, many=True)
        return Response(serializer.data)

class MyModelCreateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def post(self, request):
        # Only admin users can create new model instances
        serializer = MyModelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)



from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)



from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'created_at']



from rest_framework.permissions import BasePermission

class IsAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return obj.author == request.user
    


from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Post
from .serializers import PostSerializer
from .permissions import IsAuthorOrReadOnly # type: ignore

class PostListCreateAPIView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer



from django.urls import path
from .views import PostListCreateAPIView, PostRetrieveUpdateDestroyAPIView # type: ignore

urlpatterns = [
    path('posts/', PostListCreateAPIView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', PostRetrieveUpdateDestroyAPIView.as_view(), name='post-retrieve-update-destroy'),
]