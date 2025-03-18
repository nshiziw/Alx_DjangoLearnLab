from .models import Comment
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

# forms.py
from django import forms
from .models import Post, Tag

class PostForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(), 
        widget=forms.CheckboxSelectMultiple, 
        required=False
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']

# forms.py
from django import forms
from taggit.forms import TagWidget
from .models import Post

class PostForm(forms.ModelForm):
    # Using TagWidget to allow users to add tags
    tags = forms.CharField(widgets=TagWidget(), required=False)

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
