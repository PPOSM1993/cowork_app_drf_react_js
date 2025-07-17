from rest_framework import serializers
from .models import Resource

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = '__all__'

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("El nombre del recurso no puede estar vacío.")
        if len(value) > 255:
            raise serializers.ValidationError("El nombre no puede exceder 255 caracteres.")
        return value

    def validate_capacity(self, value):
        if value < 1:
            raise serializers.ValidationError("La capacidad debe ser al menos 1.")
        return value
