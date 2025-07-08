from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Space, Amenity, Tag, Availability
from .serializers import (
    SpaceSerializer, AmenitySerializer,
    TagSerializer, BranchSerializer,
    AvailabilitySerializer
)
from apps.branches.models import Branch
from .pagination import CustomPagination

# -------------------------
# SPACES
# -------------------------

class SpaceListCreateView(generics.ListCreateAPIView):
    queryset = Space.objects.all()
    serializer_class = SpaceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type', 'branch', 'capacity', 'is_available', 'tags', 'amenities']
    search_fields = ['name', 'description']
    ordering_fields = ['capacity', 'price_per_hour', 'name']
    ordering = ['name']
    pagination_class = CustomPagination

class SpaceRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Space.objects.all()
    serializer_class = SpaceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_destroy(self, instance):
        # Eliminación lógica: marcar como no disponible
        instance.is_available = False
        instance.save()

class SpacesByBranchView(generics.ListAPIView):
    serializer_class = SpaceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        branch_id = self.kwargs['branch_id']
        return Space.objects.filter(branch__id=branch_id)

class SpacePublicListView(generics.ListAPIView):
    queryset = Space.objects.filter(is_available=True)
    serializer_class = SpaceSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = CustomPagination

# -------------------------
# AMENITIES
# -------------------------

class AmenityListView(generics.ListAPIView):
    queryset = Amenity.objects.all()
    serializer_class = AmenitySerializer
    permission_classes = [permissions.AllowAny]

class AmenityCreateView(generics.CreateAPIView):
    queryset = Amenity.objects.all()
    serializer_class = AmenitySerializer
    permission_classes = [permissions.IsAuthenticated]

# -------------------------
# TAGS
# -------------------------

class TagListView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]

class TagCreateView(generics.CreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]

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

class AvailabilityListBySpaceView(generics.ListAPIView):
    serializer_class = AvailabilitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        space_id = self.kwargs.get('space_id')
        return Availability.objects.filter(space__id=space_id)

class AvailabilityUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer
    permission_classes = [permissions.IsAuthenticated]
