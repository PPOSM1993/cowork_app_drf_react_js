from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, DateFromToRangeFilter
from .models import Recommendation
from .serializers import RecommendationSerializer

class RecommendationFilter(FilterSet):
    created_at = DateFromToRangeFilter()

    class Meta:
        model = Recommendation
        fields = {
            'user': ['exact'],
            'recommendation_type': ['exact'],
            'is_active': ['exact'],
            'created_at': ['exact'],  # Para búsquedas exactas (además del rango)
            'title': ['icontains'],
        }

class RecommendationViewSet(viewsets.ModelViewSet):
    queryset = Recommendation.objects.all().order_by('priority', '-created_at')
    serializer_class = RecommendationSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = RecommendationFilter
    ordering_fields = ['priority', 'created_at', 'clicks', 'views']
    search_fields = ['title', 'description']
