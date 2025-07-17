from rest_framework import viewsets, permissions, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from .models import APIKey
from .serializers import APIKeySerializer


class APIKeyViewSet(viewsets.ModelViewSet):
    serializer_class = APIKeySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'key']

    def get_queryset(self):
        # Solo mostrar las API keys del usuario autenticado
        return APIKey.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Asociar la API key al usuario actual al crear
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        # Endpoint para desactivar una API key
        api_key = self.get_object()
        api_key.is_active = False
        api_key.save()
        return Response({'status': 'API key desactivada'})

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        # Endpoint para activar una API key
        api_key = self.get_object()
        api_key.is_active = True
        api_key.save()
        return Response({'status': 'API key activada'})
