# relationship_app/views.py
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render

# Function to check if the user is an admin
def is_admin(user):
    if hasattr(user, 'userprofile') and user.userprofile:
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
