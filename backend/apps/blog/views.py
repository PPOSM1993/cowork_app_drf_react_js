from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import BlogPost
from .serializers import BlogPostSerializer

class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author', 'is_published']
    search_fields = ['title', 'content']
    ordering_fields = ['published_at', 'updated_at', 'title']
    ordering = ['-published_at']

    def perform_create(self, serializer):
        # Asigna automáticamente el autor con el usuario autenticado
        serializer.save(author=self.request.user)
