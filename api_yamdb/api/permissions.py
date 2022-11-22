from rest_framework.permissions import BasePermission, SAFE_METHODS

"""Не очень хорошо, что у нас так жестко все прописано.(напр. request.user.role == 'admin')
        Стоит посмотреть на то, чтобы роль сделать атрибутом модели пользователя.
        Также настоятельно рекомендую присмотреться к @property, чтобы легко получать
        нужные данные: https://stackoverflow.com/questions/58558989/what-does-djangos-property-do
        """ 

"""Также попробуй оставить только три пермишена: админский, админ-модератор, админ-модератор-автор."""

class IsAdminOrSuperUser(BasePermission):
    """Доступ админу и суперюзеру."""

    def has_permission(self, request, view):
        return (
                not request.user.is_anonymous
                and (request.user.role == 'admin' or request.user.is_superuser)
        )


class IsAuthor(BasePermission):
    """Запрет на редактирование чужого контента."""
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsAdmimOrReadOnly(BasePermission):
    """У всех, кроме админа, права только на чтение."""
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS 
            or not request.user.is_anonymous
            and (request.user.role == 'admin' or request.user.is_superuser)
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or not request.user.is_anonymous
            and (request.user.role == 'admin' or request.user.is_superuser)
        )


class IsAdmimOrModeratorOrReadOnly(BasePermission):
    """У всех, кроме админа и модератора, права только на чтение."""

    def has_permission(self, request, view):
        return (
            request.user.is_anonymous is False
            or request.method in SAFE_METHODS
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or not request.user.is_anonymous
            and (
                request.user.role == 'admin'
                or request.user.is_superuser
                or request.user.role == 'moderator'
            )
            or obj.author == request.user
        )
