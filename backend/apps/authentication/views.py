from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth import get_user_model

from .serializers import RegisterSerializer, CustomTokenObtainPairSerializer
from .permissions import IsOwner
from rest_framework.generics import RetrieveUpdateAPIView
from .serializers import *

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


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