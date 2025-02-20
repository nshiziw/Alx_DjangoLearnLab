from .views import list_books, admin, LibraryDetailView
from django.urls import path, include

urlpatterns = [
    path('books/', list_books, name='list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    path('admin/', admin.site.urls),
    path('', include('relationship_app.urls')),  # Incl
]

from django.urls import path
from .views import register, user_login, user_logout, list_books, LibraryDetailView

urlpatterns = [
    path('', list_books, name='list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
]
