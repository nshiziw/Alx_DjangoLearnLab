from django.shortcuts import render

# Create your views here.
# accounts/views.py
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from django.contrib.auth import authenticate
from .serializers import RegisterSerializer, UserSerializer

class RegisterUserView(CreateAPIView):
    serializer_class = RegisterSerializer

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response({'error': 'Invalid credentials'}, status=400)

class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
