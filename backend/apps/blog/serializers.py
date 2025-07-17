from rest_framework import serializers
from .models import BlogPost

class BlogPostSerializer(serializers.ModelSerializer):
    author_email = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = BlogPost
        fields = ['id', 'author', 'author_email', 'title', 'content', 'published_at', 'updated_at', 'is_published']
        read_only_fields = ['published_at', 'updated_at', 'author_email']

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("El título no puede estar vacío.")
        if len(value) > 255:
            raise serializers.ValidationError("El título no puede superar los 255 caracteres.")
        return value

    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("El contenido no puede estar vacío.")
        return value
