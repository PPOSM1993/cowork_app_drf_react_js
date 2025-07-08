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
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics, status, permissions, filters

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


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def DeleteSpaces(request, pk):
    try:
        space = Space.objects.get(pk=pk)
    except Space.DoesNotExist:
        return Response({"error": "Espacio no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    space.delete()
    return Response({"message": "Espacio eliminado correctamente"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def SpacessDetail(request, pk):
    try:
        spaces = Space.objects.get(pk=pk)
    except Space.DoesNotExist:
        return Response({"error": "Espacio no encontrada"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SpaceSerializer(spaces)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SpaceSerializer(spaces, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def SearchSpace(request):
    query = request.GET.get('q', '')
    if query:
        spaces = Branch.objects.filter(
            name__icontains=query
        ) | Space.objects.filter(
            branch__icontains=query
        ) | Space.objects.filter(
            access_24_7__icontains=query
        )
    else:
        spaces = Space.objects.all()

    serializer = SpaceSerializer(spaces, many=True)
    return Response(serializer.data)
