# accounts/serializers.py
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'bio', 'profile_picture', 'followers']

class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    bio = serializers.CharField(required=False, allow_blank=True)
    profile_picture = serializers.ImageField(required=False)

    class Meta:
        model = get_user_model()
        fields = ['username', 'password', 'bio', 'profile_picture']

    def validate_password(self, value):
        # Validate password using Django's default password validation system
        validate_password(value)
        return value

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user
