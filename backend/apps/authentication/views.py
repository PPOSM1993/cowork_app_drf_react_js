from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth import get_user_model
from rest_framework.generics import RetrieveUpdateAPIView

from .serializers import RegisterSerializer, CustomTokenObtainPairSerializer, UserSerializer
from .permissions import IsOwner, HasActiveMembership

User = get_user_model()

# Registro de usuario
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

# Login personalizado con JWT
class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# Logout (revoca refresh token)
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"error": "No se envió el refresh token"}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"detail": "Sesión cerrada correctamente."}, status=status.HTTP_205_RESET_CONTENT)
        except TokenError:
            return Response({"error": "Token inválido o ya fue usado"}, status=status.HTTP_400_BAD_REQUEST)

# Ver y actualizar perfil (solo el dueño)
class ProfileDetailView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_object(self):
        # Devolver solo el perfil del usuario autenticado
        return self.request.user

# Reservar espacio (requiere membresía activa)
class ReserveSpaceView(APIView):
    permission_classes = [IsAuthenticated, HasActiveMembership]

    def post(self, request):
        user = request.user
        # Aquí agregar la lógica real para crear la reserva:
        # Ejemplo rápido (deberías validar datos, chequear disponibilidad, etc.)
        # reservation = Reservation.objects.create(user=user, ...)
        return Response({"message": f"Reserva realizada con éxito para {user.email}"}, status=status.HTTP_201_CREATED)
