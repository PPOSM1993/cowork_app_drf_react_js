from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import SupportTicket
from .serializers import SupportTicketSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


class SupportTicketListCreateView(generics.ListCreateAPIView):
    queryset = SupportTicket.objects.all().order_by('-created_at')
    serializer_class = SupportTicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'priority', 'assigned_to', 'created_by']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'priority', 'status']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class SupportTicketDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SupportTicket.objects.all()
    serializer_class = SupportTicketSerializer
    permission_classes = [permissions.IsAuthenticated]


class MyAssignedTicketsView(generics.ListAPIView):
    serializer_class = SupportTicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SupportTicket.objects.filter(assigned_to=self.request.user).order_by('-created_at')


class SearchSupportTicketsView(generics.ListAPIView):
    queryset = SupportTicket.objects.all().order_by('-created_at')
    serializer_class = SupportTicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'priority']
    ordering = ['-created_at']

class ChangeTicketStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        new_status = request.data.get('status')

        # Validar que el estado sea válido
        valid_statuses = ['open', 'in_progress', 'closed']
        if new_status not in valid_statuses:
            return Response({"error": "Estado inválido. Opciones: open, in_progress, closed."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Buscar el ticket
        try:
            ticket = SupportTicket.objects.get(pk=pk)
        except SupportTicket.DoesNotExist:
            return Response({"error": "Ticket no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        # Cambiar el estado
        ticket.status = new_status
        ticket.save()

        return Response({
            "message": f"Estado cambiado a '{new_status}'.",
            "ticket_id": ticket.id,
            "new_status": ticket.status
        }, status=status.HTTP_200_OK)