from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Resource
from .serializers import ResourceSerializer

class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['resource_type', 'is_available', 'location']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'capacity', 'created_at']
    ordering = ['name']
