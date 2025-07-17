from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q

from .models import Employee
from .serializers import EmployeeSerializer

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['first_name', 'last_name', 'rut', 'email', 'phone', 'role']
    ordering_fields = ['last_name', 'first_name', 'date_joined']
    ordering = ['last_name']

    @action(detail=False, methods=['get'], url_path='search')
    def search_employees(self, request):
        term = request.query_params.get('q', '').strip()
        if not term:
            return Response({'error': 'Debes proporcionar un parámetro ?q= para buscar.'}, status=400)

        queryset = self.get_queryset().filter(
            Q(first_name__icontains=term) |
            Q(last_name__icontains=term) |
            Q(rut__icontains=term) |
            Q(email__icontains=term) |
            Q(phone__icontains=term) |
            Q(role__icontains=term)
        )

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
