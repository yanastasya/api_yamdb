from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrSuperUser(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_anonymous:
            if request.user.role == 'admin' or request.user.is_superuser:
                return True
        return False


# class IsAuthor(BasePermission):

#     def has_object_permission(self, request, view, obj):
#         return obj.author == request.user


# class ForObjectIsAdmimrReadOnly(BasePermission):
    
#     def has_object_permission(self, request, view, obj):
#         return request.user.role == 'admin' or request.user.is_superuser


# class IsModerator(BasePermission):
    
#     def has_object_permission(self, request, view, obj):
#         return request.user.role == 'moderator'


class IsAdmimOrReadOnly(BasePermission):
    
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

