
from rest_framework import permissions

class IsRoleAdminOrSuperUser(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_anonymous:
            if request.user.role == 'admin' or request.user.is_superuser:
                return True
        return False