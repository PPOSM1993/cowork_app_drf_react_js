from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from .models import *

User = get_user_model()

class EmailUsernameRutBackend(ModelBackend):
    """
    Permite autenticación usando email, username o RUT.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = None

        # Buscar por email, username o rut
        try:
            user = User.objects.get(
                models.Q(email__iexact=username) |
                models.Q(username__iexact=username) |
                models.Q(rut__iexact=username)
            )
        except User.DoesNotExist:
            return None

        # Verificar contraseña
        if user and user.check_password(password):
            return user

        return None
