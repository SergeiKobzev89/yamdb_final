from rest_framework import permissions
from reviews.models import User


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_admin


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.username == request.user.username


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Управление произведениями доступно только админу,
    остальные пользователи в режиме read only.
    """
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_admin
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_admin
        )


class ReviewCommentPermissions(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method == 'POST':
            return not request.user.is_anonymous()

        if request.method in ('PATCH', 'DELETE'):
            return (
                request.user == obj.author
                or request.user.role == User.ADMIN
                or request.user.role == User.MODERATOR
            )

        if request.method in permissions.SAFE_METHODS:
            return True

        return False


class IsAdminOrSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return bool(
                request.user.is_admin
                or request.user.role == User.ADMIN
            )

        return False


class PermissionMixin:
    def get_permissions(self):
        permission_classes = []

        if self.action in ('list', 'retrieve'):
            permission_classes = [permissions.AllowAny]

        if self.action in ('create', 'destroy', 'update', 'partial_update'):
            permission_classes = [permissions.IsAdminUser]

        return [permission() for permission in permission_classes]
