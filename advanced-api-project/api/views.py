from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer

# List all books (Allow anyone to view)
class BookListView(generics.ListAPIView):
    """List all books"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

# Retrieve a single book by ID
class BookDetailView(generics.RetrieveAPIView):
    """Retrieve a specific book"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

# Create a new book (Only for authenticated users)
class BookCreateView(generics.CreateAPIView):
    """Create a new book and automatically set the author to the logged-in user"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Assuming the user is also an author (extend this logic as needed)
        author, created = Author.objects.get_or_create(name=self.request.user.username)
        serializer.save(author=author)


# Update an existing book (Only for authenticated users)
class BookUpdateView(generics.UpdateAPIView):
    """Update a book"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

# Delete a book (Only for authenticated users)
class BookDeleteView(generics.DestroyAPIView):
    """Delete a book"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


class BookUpdateView(generics.UpdateAPIView):
    """Update a book"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthorOrReadOnly]
