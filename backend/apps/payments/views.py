from rest_framework import generics, permissions, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import Payment
from .serializers import PaymentSerializer
from apps.customers.models import Customer
from apps.reservations.models import Reservation
from .pagination import CustomPagination
from rest_framework.permissions import IsAuthenticated

# -------------------------
# PAYMENTS
# -------------------------

class PaymentListCreateView(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['customer', 'reservation', 'status', 'method']
    search_fields = ['notes']
    ordering_fields = ['amount', 'payment_date']
    ordering = ['-payment_date']
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        serializer.save()

class PaymentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        # Eliminación lógica si es necesario (por ahora, eliminación normal)
        instance.delete()


# -------------------------
# CUSTOM API VIEWS (opcional)
# -------------------------

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def PaymentsByCustomer(request, customer_id):
    payments = Payment.objects.filter(customer__id=customer_id)
    serializer = PaymentSerializer(payments, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def PaymentsByReservation(request, reservation_id):
    payments = Payment.objects.filter(reservation__id=reservation_id)
    serializer = PaymentSerializer(payments, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def SearchPayments(request):
    query = request.GET.get('q', '')
    if query:
        payments = Payment.objects.filter(
            transaction_id__icontains=query
        ) | Payment.objects.filter(
            status__icontains=query
        ) | Payment.objects.filter(
            payment_method__icontains=query
        ) | Payment.objects.filter(
            customer__first_name__icontains=query
        ) | Payment.objects.filter(
            customer__last_name__icontains=query
        )
    else:
        payments = Payment.objects.all()

    serializer = PaymentSerializer(payments, many=True)
    return Response(serializer.data)