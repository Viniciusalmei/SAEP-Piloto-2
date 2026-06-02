from rest_framework.permissions import BasePermission, SAFE_METHODS

class ApenasAdministrador(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.tipo == 'administrador'

class OperadorOuAdmin(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.method == 'DELETE':
            return request.user.tipo == 'administrador'
        return True