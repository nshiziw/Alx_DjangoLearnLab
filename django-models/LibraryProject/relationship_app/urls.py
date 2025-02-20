# relationship_app/urls.py
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', 'relationship_app.views.list_books', name='list_books'),
    path('library/<int:pk>/', 'relationship_app.views.LibraryDetailView', name='library_detail'),
    path('register/', 'relationship_app.views.register', name='register'),  # This is now using 'views.register' as a string
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
]
