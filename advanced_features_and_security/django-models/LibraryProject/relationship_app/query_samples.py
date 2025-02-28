import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')  # Update this to match your project name
django.setup()

from relationship_app.models import Author, Book, Library, Librarian


# Query all books by a specific author
def books_by_author(author_name):
    try:
        author = Author.objects.get(name=author_name)
        return Book.objects.filter(author=author)
    except Author.DoesNotExist:
        return f"Author '{author_name}' does not exist."


# List all books in a library
def books_in_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        return library.books.all()
    except Library.DoesNotExist:
        return f"Library '{library_name}' does not exist."


# Retrieve the librarian for a library
def librarian_of_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        librarian = Librarian.objects.get(library=library)  # Correct usage here! ✅
        return librarian
    except (Library.DoesNotExist, Librarian.DoesNotExist):
        return f"No librarian found for library '{library_name}'."


# Example usage
if __name__ == "__main__":
    print("Books by Author 'John Doe':", books_by_author('John Doe'))
    print("Books in 'Central Library':", books_in_library('Central Library'))
    print("Librarian of 'Central Library':", librarian_of_library('Central Library'))
