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
from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import get_user_model

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


@api_view(['POST'])
def follow_user(request, user_id):
    user_to_follow = get_user_model().objects.filter(id=user_id).first()
    if not user_to_follow:
        return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    
    if user_to_follow == request.user:
        return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

    request.user.following.add(user_to_follow)
    return Response({"detail": f"Now following {user_to_follow.username}."}, status=status.HTTP_200_OK)

@api_view(['POST'])
def unfollow_user(request, user_id):
    user_to_unfollow = get_user_model().objects.filter(id=user_id).first()
    if not user_to_unfollow:
        return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    if user_to_unfollow == request.user:
        return Response({"detail": "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)

    request.user.following.remove(user_to_unfollow)
    return Response({"detail": f"Unfollowed {user_to_unfollow.username}."}, status=status.HTTP_200_OK)
