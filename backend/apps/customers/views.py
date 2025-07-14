from rest_framework import generics, permissions, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from apps.customers.models import Customer
from apps.customers.serializers import CustomerSerializer
from .pagination import CustomPagination

# -------------------------
# CUSTOMERS
# -------------------------

class CustomerListCreateView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['customer_type', 'region', 'city']
    search_fields = ['first_name', 'last_name', 'email', 'phone', 'tax_id', 'company_user']
    ordering_fields = ['first_name', 'last_name', 'created_at']
    ordering = ['first_name']
    pagination_class = CustomPagination


class CustomerRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]


# 🔎 Búsqueda personalizada (por nombre, email, empresa)
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def SearchCustomer(request):
    query = request.GET.get('q', '').strip()
    if query:
        customers = Customer.objects.filter(
            first_name__icontains=query
        ) | Customer.objects.filter(
            last_name__icontains=query
        ) | Customer.objects.filter(
            email__icontains=query
        ) | Customer.objects.filter(
            company_user__icontains=query
        )
    else:
        customers = Customer.objects.all()

    serializer = CustomerSerializer(customers, many=True)
    return Response(serializer.data)


# 🔥 Eliminación directa (si prefieres una vista API directa tipo función)
@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def DeleteCustomer(request, pk):
    try:
        customer = Customer.objects.get(pk=pk)
    except Customer.DoesNotExist:
        return Response({"error": "Cliente no encontrado."}, status=status.HTTP_404_NOT_FOUND)

    customer.delete()
    return Response({"message": "Cliente eliminado correctamente."}, status=status.HTTP_204_NO_CONTENT)


# 📄 Detalle + Update con función
@api_view(['GET', 'PUT'])
@permission_classes([permissions.IsAuthenticated])
def CustomerDetail(request, pk):
    try:
        customer = Customer.objects.get(pk=pk)
    except Customer.DoesNotExist:
        return Response({"error": "Cliente no encontrado."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CustomerSerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
