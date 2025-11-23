from rest_framework import permissions

class IsAdminForDeleteAuthenticatedForWriteOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == 'DELETE':
            return bool(request.user and request.user.is_staff)
        return bool(request.user and request.user.is_authenticated)
