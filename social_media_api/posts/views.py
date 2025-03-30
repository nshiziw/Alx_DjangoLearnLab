# posts/views.py
from django.shortcuts import render
from rest_framework import viewsets, permissions, filters
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def update(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            raise PermissionDenied("You cannot edit this post.")
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            raise PermissionDenied("You cannot delete this post.")
        return super().destroy(request, *args, **kwargs)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def update(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.author != request.user:
            raise PermissionDenied("You cannot edit this comment.")
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.author != request.user:
            raise PermissionDenied("You cannot delete this comment.")
        return super().destroy(request, *args, **kwargs)

class FeedViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        # Get the list of users the current user is following
        following_users = request.user.following.all()

        # Get the posts from the followed users
        posts = Post.objects.filter(author__in=following_users).order_by('-created_at')

        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Post, Like
from .serializers import PostSerializer, LikeSerializer
from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['POST'])
    def like(self, request, pk=None):
        post = self.get_object()
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if created:
            # Create a notification
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb="liked your post",
                target=post
            )
            return Response({"message": "Post liked"}, status=status.HTTP_201_CREATED)
        return Response({"message": "Already liked"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['POST'])
    def unlike(self, request, pk=None):
        post = self.get_object()
        like = Like.objects.filter(user=request.user, post=post)
        if like.exists():
            like.delete()
            return Response({"message": "Post unliked"}, status=status.HTTP_200_OK)
        return Response({"message": "You haven't liked this post"}, status=status.HTTP_400_BAD_REQUEST)


from django.shortcuts import render
from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from django.shortcuts import get_object_or_404  # ✅ Ensure get_object_or_404 is imported

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def update(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            raise PermissionDenied("You cannot edit this post.")
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            raise PermissionDenied("You cannot delete this post.")
        return super().destroy(request, *args, **kwargs)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def update(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.author != request.user:
            raise PermissionDenied("You cannot edit this comment.")
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.author != request.user:
            raise PermissionDenied("You cannot delete this comment.")
        return super().destroy(request, *args, **kwargs)

class FeedViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        # Get the list of users the current user is following
        followed_users = request.user.following.all()
        # Include the current user in the feed (optional)
        followed_users = followed_users | request.user.followers.all()

        # Get the posts from the followed users
        posts = Post.objects.filter(author__in=followed_users).order_by('-created_at')

        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

class LikePostView(generics.GenericAPIView):  # ✅ Using GenericAPIView
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)  # ✅ Ensure get_object_or_404 is used
        if request.user in post.likes.all():
            return Response({"detail": "You already liked this post."}, status=400)
        post.likes.add(request.user)
        return Response({"detail": "Post liked successfully!"}, status=200)
