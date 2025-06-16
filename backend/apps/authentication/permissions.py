from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    """
    Permite acceso solo al usuario dueño del objeto.
    """
    def has_object_permission(self, request, view, obj):
        return obj == request.user


class IsStaffOrReadOnly(BasePermission):
    """
    Permite acceso de escritura solo a staff, lectura a todos.
    """
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return request.user and request.user.is_staff
