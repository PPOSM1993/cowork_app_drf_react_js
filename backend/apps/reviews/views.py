from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Review
from .serializers import ReviewSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['user', 'content_type', 'object_id', 'rating', 'is_approved']
    ordering_fields = ['created_at', 'rating']
    ordering = ['-created_at']
    search_fields = ['comment']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
