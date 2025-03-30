from django.test import TestCase

# Create your tests here.

# posts/tests.py
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from .models import Post, Comment

class PostCommentTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.post = Post.objects.create(author=self.user, title="Test Post", content="Test content")
        self.comment = Comment.objects.create(post=self.post, author=self.user, content="Test comment")

    def test_create_post(self):
        data = {'title': 'New Post', 'content': 'Post content'}
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post('/api/posts/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_comment(self):
        data = {'content': 'New comment', 'post': self.post.id}
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post('/api/comments/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
