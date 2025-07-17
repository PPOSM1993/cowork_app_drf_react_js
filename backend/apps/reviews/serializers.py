from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    user_email = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Review
        fields = [
            'id', 'user', 'user_email',
            'content_type', 'object_id',
            'rating', 'comment',
            'created_at', 'updated_at', 'is_approved',
        ]
        read_only_fields = ['created_at', 'updated_at', 'user_email', 'is_approved']

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("La calificación debe estar entre 1 y 5.")
        return value

    def validate(self, data):
        # Validar que content_type sea uno permitido
        allowed_models = ['space', 'service', 'reservation']  # Nombres de modelos permitidos (minúsculas)
        content_type = data.get('content_type')
        if content_type.model not in allowed_models:
            raise serializers.ValidationError(
                {'content_type': f"Tipo de contenido no permitido. Solo: {allowed_models}"}
            )
        return data

    def create(self, validated_data):
        # Asignar automáticamente usuario autenticado si no viene en request
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['user'] = request.user
        return super().create(validated_data)
