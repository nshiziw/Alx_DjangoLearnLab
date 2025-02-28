from django.contrib.auth.models import AbstractBaseUser

class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    # ... additional fields and methods as required ...


from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True)
    # ... additional fields as needed ...

from django.contrib.auth.backends import BaseBackend

class EmailBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        # Implement logic to authenticate user using email and password
        # ...

    def get_user(self, user_id):
        # Implement logic to retrieve user based on user ID
        # ...


AUTHENTICATION_BACKENDS = [
    'path.to.EmailBackend',  # Your custom backend
    'django.contrib.auth.backends.ModelBackend',  # Keep the default backend as a fallback
]


from django.contrib.auth.models import Permission

# Get the permission
permission = Permission.objects.get(codename='add_post')

# Assign permission to a user
user.user_permissions.add(permission)

# Assign permission to a group
group.permissions.add(permission)



def my_view(request):
    if request.user.has_perm('app_name.add_post'):
        # Allow user to create a new post
        ...
    else:
        # Deny access or show an error message
        ...



# {% if perms.app_name.add_post %}
#     <a href="{% url 'create_post' %}">Create New Post</a>
# {% endif %}


class Post(models.Model):
    # ... other fields ...

    class Meta:
        permissions = [
            ("can_publish_post", "Can publish post"),
        ]