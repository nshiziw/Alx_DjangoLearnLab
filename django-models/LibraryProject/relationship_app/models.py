from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Library(models.Model):
    name = models.CharField(max_length=255)
    books = models.ManyToManyField(Book)

    def __str__(self):
        return self.name

class Librarian(models.Model):
    name = models.CharField(max_length=255)
    library = models.OneToOneField(Library, on_delete=models.CASCADE)

    def __str__(self):
        return self.name




from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    # Linking to the User model via OneToOneField
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Defining role choices
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('librarian', 'Librarian'),
        ('member', 'Member'),
    ]
    
    # Role field with choices
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    
    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"
