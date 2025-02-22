# relationship_app/urls.py
from django.urls import path
from .views import list_books
from django.contrib.auth.views import LoginView, LogoutView
from .views import admin_view, librarian_view, member_view
from .views import add_book, edit_book, delete_book, list_books

urlpatterns = [
    path('', 'relationship_app.views.list_books', name='list_books'),
    path('library/<int:pk>/', 'relationship_app.views.LibraryDetailView', name='library_detail'),
    path('register/', 'relationship_app.views.register', name='register'),  # This is now using 'views.register' as a string
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('', list_books, name='list_books'),  # Assuming this is already defined for listing books
    path('add/', add_book, name='add_book'),  # URL for adding a book
    path('edit/<int:book_id>/', edit_book, name='edit_book'),  # URL for editing a specific book
    path('delete/<int:book_id>/', delete_book, name='delete_book'),  # URL for deleting a specific book
]



urlpatterns = [
    path('admin/', admin_view, name='admin_view'),
    path('librarian/', librarian_view, name='librarian_view'),
    path('member/', member_view, name='member_view'),
]