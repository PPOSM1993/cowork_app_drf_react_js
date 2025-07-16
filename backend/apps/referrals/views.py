from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Referral
from .serializers import ReferralSerializer
from .pagination import CustomPagination  # si usas paginación personalizada

# Listar y crear referencias
class ReferralListCreateView(generics.ListCreateAPIView):
    queryset = Referral.objects.all().order_by('-created_at')
    serializer_class = ReferralSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'referrer']
    search_fields = ['referred_email', 'referral_code']
    ordering_fields = ['created_at', 'status']
    ordering = ['-created_at']
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        serializer.save(referrer=self.request.user)

# Obtener, actualizar y eliminar una referencia específica
class ReferralDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Referral.objects.all()
    serializer_class = ReferralSerializer
    permission_classes = [permissions.IsAuthenticated]

# Vista especializada: listar solo referencias activas del usuario autenticado
class MyActiveReferralsView(generics.ListAPIView):
    serializer_class = ReferralSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Referral.objects.filter(
            referrer=self.request.user,
            status='pending'
        ).order_by('-created_at')
