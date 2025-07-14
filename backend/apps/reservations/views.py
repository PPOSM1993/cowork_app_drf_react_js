from rest_framework import generics, permissions, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Reservation
from .serializers import ReservationSerializer
from .pagination import CustomPagination
from rest_framework.permissions import IsAuthenticated

# -------------------------
# RESERVATIONS
# -------------------------

class ReservationListCreateView(generics.ListCreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'customer', 'space']
    search_fields = ['customer__first_name', 'customer__last_name', 'space__name']
    ordering_fields = ['start_datetime', 'end_datetime', 'created_at']
    ordering = ['start_datetime']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ReservationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]


# Vista opcional: Reservas activas de un cliente específico
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def ReservationsByCustomer(request, customer_id):
    reservations = Reservation.objects.filter(customer__id=customer_id, status='active')
    serializer = ReservationSerializer(reservations, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def SearchReservations(request):
    query = request.GET.get('q', '')
    if query:
        reservations = Reservation.objects.filter(
            code__icontains=query
        ) | Reservation.objects.filter(
            status__icontains=query
        ) | Reservation.objects.filter(
            customer__first_name__icontains=query
        ) | Reservation.objects.filter(
            customer__last_name__icontains=query
        )
    else:
        reservations = Reservation.objects.all()

    serializer = ReservationSerializer(reservations, many=True)
    return Response(serializer.data)