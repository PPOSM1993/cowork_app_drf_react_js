from rest_framework import serializers
from .models import APIKey

class APIKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = APIKey
        fields = ['id', 'key', 'user', 'name', 'is_active', 'created_at', 'expires_at', 'usage_limit_per_day']
        read_only_fields = ['id', 'key', 'created_at']

    def validate_usage_limit_per_day(self, value):
        if value <= 0:
            raise serializers.ValidationError("El límite de uso por día debe ser mayor que cero.")
        return value

    def validate(self, data):
        expires_at = data.get('expires_at')
        if expires_at and expires_at <= serializers.DateTimeField().to_internal_value(self.context['request'].timestamp()):
            raise serializers.ValidationError("La fecha de expiración debe ser en el futuro.")
        return data
