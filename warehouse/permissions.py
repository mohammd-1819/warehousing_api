from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsReadOnlyUser(BasePermission):
    """
    Custom permission to only allow read-only access to users.
    """

    def has_permission(self, request, view):
        # Allow access if the request method is in SAFE_METHODS (GET, HEAD, OPTIONS)
        return request.method in SAFE_METHODS
