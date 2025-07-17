from rest_framework import serializers
from .models import Recommendation
from django.utils import timezone

class RecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendation
        fields = '__all__'
        read_only_fields = ['clicks', 'views', 'created_at']

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("El título no puede estar vacío o solo contener espacios.")
        if len(value) > 255:
            raise serializers.ValidationError("El título no puede exceder 255 caracteres.")
        return value

    def validate_priority(self, value):
        if value < 1:
            raise serializers.ValidationError("La prioridad debe ser un número positivo mayor o igual a 1.")
        return value

    def validate_expires_at(self, value):
        if value and value <= timezone.now():
            raise serializers.ValidationError("La fecha de expiración debe ser en el futuro.")
        return value

    def validate_recommendation_type(self, value):
        valid_types = [choice[0] for choice in Recommendation.RECOMMENDATION_TYPES]
        if value not in valid_types:
            raise serializers.ValidationError(f"Tipo de recomendación inválido. Debe ser uno de {valid_types}.")
        return value

    def validate(self, data):
        """
        Validación global para reglas cruzadas:
        Si el tipo no es 'custom', entonces 'related_object_id' es obligatorio.
        """
        recommendation_type = data.get('recommendation_type', getattr(self.instance, 'recommendation_type', None))
        related_object_id = data.get('related_object_id', getattr(self.instance, 'related_object_id', None))

        if recommendation_type != 'custom' and related_object_id is None:
            raise serializers.ValidationError({
                'related_object_id': "Este campo es obligatorio para tipos de recomendación distintos a 'custom'."
            })

        if recommendation_type == 'custom' and related_object_id is not None:
            raise serializers.ValidationError({
                'related_object_id': "Este campo debe estar vacío para tipo 'custom'."
            })

        return data
