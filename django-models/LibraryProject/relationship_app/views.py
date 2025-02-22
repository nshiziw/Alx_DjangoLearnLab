# relationship_app/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import user_passes_test
from .models import Library, Book, UserProfile
from django.views.generic.detail import DetailView


# Function-based view to list all books
def list_books(request):
    books = Book.objects.all()  # Explicitly using Book.objects.all() as required
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-based view to display library details
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

# User registration view
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after registration
            return redirect('list_books')  # Redirect to your home or book list page
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

# User login view
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('list_books')  # Redirect to book list after login
    else:
        form = AuthenticationForm()
    return render(request, 'relationship_app/login.html', {'form': form})

# User logout view
def user_logout(request):
    logout(request)
    return redirect('login')


# Function to check if the user is an admin
def is_admin(user):
    if hasattr(user, 'userprofile') and user.userprofile:
        print(f"User role: {user.userprofile.role}")  # Debugging statement
        return user.userprofile.role == 'admin'
    return False

# Function to check if the user is a librarian
def is_librarian(user):
    if hasattr(user, 'userprofile') and user.userprofile:
        return user.userprofile.role == 'librarian'
    return False

# Function to check if the user is a member
def is_member(user):
    if hasattr(user, 'userprofile') and user.userprofile:
        return user.userprofile.role == 'member'
    return False

# Admin view - only accessible by admin users
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

# Librarian view - only accessible by librarian users
@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

# Member view - only accessible by member users
@user_passes_test(is_member)
def member_view(request):
    return render(request, 'relationship_app/member_view.html')