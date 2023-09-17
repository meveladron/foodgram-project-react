from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Пользовательское разрешение для
    изменения данных только суперпользователем
    """
    def has_permission(self, request, view):
        is_safe_method = request.method in permissions.SAFE_METHODS
        is_admin_or_superuser = request.user.is_authenticated and (
            request.user.is_admin or request.user.is_superuser
        )
        return is_safe_method or is_admin_or_superuser

    def has_object_permission(self, request, view, obj):
        is_safe_method = request.method in permissions.SAFE_METHODS
        is_admin_or_superuser = request.user.is_authenticated and (
            request.user.is_admin or request.user.is_superuser
        )
        return is_safe_method or is_admin_or_superuser


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Пользовательское разрешение для изменения данных только авторам."""
    def has_object_permission(self, request, view, target_object):
        return (
            request.method in permissions.SAFE_METHODS
            or target_object.author == request.user
        )
