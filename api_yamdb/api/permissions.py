from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrSuperUser(BasePermission):
    """Доступ админу и суперюзеру."""

    def has_permission(self, request, view):
        if not request.user.is_anonymous:
            if request.user.role == 'admin' or request.user.is_superuser:
                return True
        return False


class IsAuthor(BasePermission):
    """Запрет на редактирование чужого контента."""
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsAdmimOrReadOnly(BasePermission):
    """У всех, кроме админа, права только на чтение."""
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if not request.user.is_anonymous:
            if request.user.role == 'admin' or request.user.is_superuser:
                return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if not request.user.is_anonymous:
            if request.user.role == 'admin' or request.user.is_superuser:
                return True
        return False


class IsAdmimOrModeratorOrReadOnly(BasePermission):
    """У всех, кроме админа и модератора, права только на чтение."""
    def has_permission(self, request, view):
        return (
            request.user.is_anonymous is False
            or request.method in SAFE_METHODS
        )

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if not request.user.is_anonymous:
            if (
                request.user.role == 'admin'
                or request.user.is_superuser
                or request.user.role == 'moderator'
            ):
                return True
        if obj.author == request.user:
            return True
        return False
