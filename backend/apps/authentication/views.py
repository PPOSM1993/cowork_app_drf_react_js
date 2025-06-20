from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from .tokens import account_activation_token
from .serializers import RegisterSerializer, CustomTokenObtainPairSerializer
from .permissions import *
from rest_framework.generics import RetrieveUpdateAPIView
from .serializers import *
from django.utils.http import urlsafe_base64_decode
from .utils import send_confirmation_email


User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
    
    def perform_create(self, serializer):
        print("Registrando usuario...")
        user = serializer.save(is_active=False)
        print("Usuario creado:", user.email)
        send_confirmation_email(self.request, user)
        print("Email enviado a:", user.email)
class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"error": "Usuario no autenticado"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"error": "No se envió el refresh token"}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"detail": "Sesión cerrada correctamente."}, status=status.HTTP_205_RESET_CONTENT)
        except TokenError:
            return Response({"error": "Token inválido o ya fue usado"}, status=status.HTTP_400_BAD_REQUEST)

class ProfileDetailView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwner]
    
    def get_object(self):
        return self.request.user

class ReserveSpaceView(APIView):
    permission_classes = [IsAuthenticated, HasActiveMembership]

    def post(self, request):
        user = request.user
        # Aquí lógica para reservar espacio (pendiente implementación)
        return Response({"message": f"Reserva realizada con éxito para {user.email}"}, status=status.HTTP_201_CREATED)
    
class ConfirmEmailView(APIView):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            return HttpResponse('El enlace no es válido.', content_type='text/plain')

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return HttpResponse('¡Tu cuenta ha sido activada con éxito!', content_type='text/plain')
        else:
            return HttpResponse('El enlace de activación no es válido o ha expirado.', content_type='text/plain')

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(is_active=False)  # ⚠️ Desactiva hasta confirmar por correo
            send_confirmation_email(request, user)
            return Response({"message": "Usuario creado. Revisa tu correo para activar la cuenta."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)