# relationship_app/urls.py
from django.urls import path
from .views import list_books, add_book, edit_book, delete_book, admin_view, librarian_view, member_view
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    # Auth-related paths
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('register/', 'relationship_app.views.register', name='register'),

    # Book management paths
    path('add/', add_book, name='add_book'),  # URL for adding a book
    path('edit/<int:book_id>/', edit_book, name='edit_book/'),  # URL for editing a specific book
    path('delete/<int:book_id>/', delete_book, name='delete_book'),  # URL for deleting a specific book

    # Views for different roles
    path('admin/', admin_view, name='admin_view'),
    path('librarian/', librarian_view, name='librarian_view'),
    path('member/', member_view, name='member_view'),

    # Other paths
    path('library/<int:pk>/', 'relationship_app.views.LibraryDetailView', name='library_detail'),
]
