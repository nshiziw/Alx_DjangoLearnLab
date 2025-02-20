from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "publication_year")  # Columns shown in list view
    search_fields = ("title", "author")  # Enables search by title and author
    list_filter = ("publication_year",)  # Adds filtering by publication year
