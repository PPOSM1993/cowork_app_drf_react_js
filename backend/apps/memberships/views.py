from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Membership
from .serializers import MembershipSerializer
from .pagination import CustomPagination

class MembershipListCreateView(generics.ListCreateAPIView):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'price', 'is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'name', 'duration_days']
    ordering = ['price']

class MembershipRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer
    permission_classes = [permissions.IsAuthenticated]


class MembershipPublicListView(generics.ListAPIView):
    queryset = Membership.objects.filter(is_active=True)
    serializer_class = MembershipSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = CustomPagination
