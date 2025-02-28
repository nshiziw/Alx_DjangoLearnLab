from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "publication_year")  # Columns shown in list view
    search_fields = ("title", "author")  # Enables search by title and author
    list_filter = ("publication_year",)  # Adds filtering by publication year


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'date_of_birth', 'profile_photo', 'is_staff']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'date_of_birth', 'profile_photo')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {'fields': ('username', 'email', 'password1', 'password2')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'date_of_birth', 'profile_photo')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)



from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import Book

# Function to create groups and assign permissions
def setup_groups():
    # Create groups if they don't exist
    editors, _ = Group.objects.get_or_create(name="Editors")
    viewers, _ = Group.objects.get_or_create(name="Viewers")
    admins, _ = Group.objects.get_or_create(name="Admins")

    # Get Book model permissions
    content_type = ContentType.objects.get_for_model(Book)
    permissions = {
        "can_view": Permission.objects.get(content_type=content_type, codename="can_view"),
        "can_create": Permission.objects.get(content_type=content_type, codename="can_create"),
        "can_edit": Permission.objects.get(content_type=content_type, codename="can_edit"),
        "can_delete": Permission.objects.get(content_type=content_type, codename="can_delete"),
    }

    # Assign permissions
    viewers.permissions.set([permissions["can_view"]])
    editors.permissions.set([permissions["can_view"], permissions["can_edit"], permissions["can_create"]])
    admins.permissions.set(permissions.values())

# Run setup on startup
setup_groups()

# Register the model
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "published_date")
