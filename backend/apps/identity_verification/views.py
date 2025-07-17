from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils.timezone import now

from .models import IdentityVerification
from .serializers import IdentityVerificationSerializer


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Solo el usuario dueño o un administrador puede acceder a un registro.
    """

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.user == request.user


class IdentityVerificationViewSet(viewsets.ModelViewSet):
    """
    Gestión de las solicitudes de verificación de identidad.
    """
    queryset = IdentityVerification.objects.all().select_related('user')
    serializer_class = IdentityVerificationSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return IdentityVerification.objects.all()
        return IdentityVerification.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def approve(self, request, pk=None):
        """
        Endpoint: /api/identity_verification/{id}/approve/
        Solo administradores pueden aprobar la verificación.
        """
        verification = self.get_object()
        verification.status = 'approved'
        verification.reviewed_at = now()
        verification.review_comments = request.data.get('review_comments', 'Aprobado automáticamente.')
        verification.save()
        return Response({'status': 'Aprobado'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def reject(self, request, pk=None):
        """
        Endpoint: /api/identity_verification/{id}/reject/
        Solo administradores pueden rechazar la verificación.
        """
        verification = self.get_object()
        verification.status = 'rejected'
        verification.reviewed_at = now()
        verification.review_comments = request.data.get('review_comments', 'Rechazado.')
        verification.save()
        return Response({'status': 'Rechazado'}, status=status.HTTP_200_OK)
