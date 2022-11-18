
from rest_framework import permissions

class RoleAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_anonymous == False and request.user.role == 'admin'
