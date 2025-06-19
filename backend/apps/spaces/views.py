from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Space, Amenity, Tag, Branch, Availability
from .serializers import (
    SpaceSerializer, AmenitySerializer,
    TagSerializer, BranchSerializer,
    AvailabilitySerializer
)

from .pagination import CustomPagination

# -------------------------
# SPACES
# -------------------------

class SpaceListCreateView(generics.ListCreateAPIView):
    queryset = Space.objects.all()
    serializer_class = SpaceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # Filtros y búsqueda
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type', 'branch', 'capacity', 'status']
    search_fields = ['name', 'description']
    ordering_fields = ['capacity', 'price_per_hour', 'name']
    ordering = ['name']
    pagination_class = CustomPagination
class SpaceRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Space.objects.all()
    serializer_class = SpaceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# -------------------------
# AMENITIES
# -------------------------

class AmenityListView(generics.ListAPIView):
    queryset = Amenity.objects.all()
    serializer_class = AmenitySerializer
    permission_classes = [permissions.AllowAny]

# -------------------------
# TAGS
# -------------------------

class TagListView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]

# -------------------------
# BRANCHES
# -------------------------

class BranchListView(generics.ListAPIView):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [permissions.AllowAny]

# -------------------------
# AVAILABILITY
# -------------------------

class AvailabilityCreateView(generics.CreateAPIView):
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer
    permission_classes = [permissions.IsAuthenticated]
