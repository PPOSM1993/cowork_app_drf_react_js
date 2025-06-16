from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Permite acceso sólo al dueño del objeto (por ejemplo, su propio perfil).
    """
    def has_object_permission(self, request, view, obj):
        return obj == request.user


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permite acceso completo sólo a admins. Lectura para otros usuarios.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class HasActiveMembership(permissions.BasePermission):
    """
    Permite acceso sólo a usuarios con una membresía activa.
    Requiere una relación user.membership con is_active.
    """
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and hasattr(user, 'membership') and user.membership.is_active


class IsSupportAgent(permissions.BasePermission):
    """
    Permite acceso sólo a usuarios con rol de agente de soporte.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, 'is_support', False)


class IsVerifiedUser(permissions.BasePermission):
    """
    Permite acceso sólo a usuarios verificados (por ejemplo, por verificación de identidad).
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, 'is_verified', False)
