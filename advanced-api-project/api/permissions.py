from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    """Custom permission: Authors can edit their books, others can only read"""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True  # Allow read-only access
        return obj.author.name == request.user.username  # Only author can modify
