from .views import list_books, admin, LibraryDetailView
from django.urls import path, include

urlpatterns = [
    path('books/', list_books, name='list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    path('admin/', admin.site.urls),
    path('', include('relationship_app.urls')),  # Incl
]
