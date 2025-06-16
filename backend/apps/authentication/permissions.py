from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwner(BasePermission):
    """
    Permite acceso solo si el usuario es el dueño del objeto.
    """
    def has_object_permission(self, request, view, obj):
        return obj == request.user


class IsStaffOrReadOnly(BasePermission):
    """
    Solo el staff puede escribir, los demás solo pueden leer.
    """
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS or
            request.user and request.user.is_staff
        )


class IsVerifiedUser(BasePermission):
    """
    Permite acceso solo a usuarios con verificación de identidad.
    Asume que el modelo User tiene un campo 'is_verified'.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_verified


class HasActiveMembership(BasePermission):
    """
    Permite acceso solo si el usuario tiene una membresía activa.
    Asume una relación `user.membership.is_active`
    """
    def has_permission(self, request, view):
        user = request.user
        return (
            user and user.is_authenticated and
            hasattr(user, 'membership') and
            user.membership.is_active
        )


class IsAdminOrSelf(BasePermission):
    """
    Permite a los admin acceder a todo, o a los usuarios modificar solo su propio perfil.
    """
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj == request.user