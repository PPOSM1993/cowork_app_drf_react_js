from rest_framework import generics, permissions, status, filters
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Report
from .serializers import ReportSerializer
from .pagination import CustomPagination


# Listar y crear reportes
class ReportListCreateView(generics.ListCreateAPIView):
    queryset = Report.objects.all().order_by('-generated_at')
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

# Obtener, actualizar y eliminar reportes
class ReportDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]

# Generar manualmente un reporte (si el modelo tiene esa función)
class GenerateReportView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            report = Report.objects.get(pk=pk)
            report.generate_report()  # Suponiendo que tu modelo tiene este método
            report.save()
            return Response({"message": "Reporte generado exitosamente."}, status=status.HTTP_200_OK)
        except Report.DoesNotExist:
            return Response({"error": "Reporte no encontrado."}, status=status.HTTP_404_NOT_FOUND)

# Buscar reportes con filtros y ordenamiento
class ReportSearchView(generics.ListAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'report_type', 'generated_by']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    pagination_class = CustomPagination
