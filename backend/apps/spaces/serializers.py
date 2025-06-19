from rest_framework import serializers
from .models import Space, Amenity, Tag, Branch, Availability
from django.utils import timezone
from datetime import time

class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ['id', 'name', 'icon']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ['id', 'name', 'address', 'city', 'region', 'phone', 'email', 'image']

class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = ['id', 'day_of_week', 'start_time', 'end_time']

    def validate(self, data):
        if data['start_time'] >= data['end_time']:
            raise serializers.ValidationError("La hora de inicio debe ser anterior a la hora de fin")
        return data

class SpaceSerializer(serializers.ModelSerializer):
    amenities = AmenitySerializer(many=True, read_only=True)
    amenities_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Amenity.objects.all(), write_only=True, source='amenities'
    )

    tags = TagSerializer(many=True, read_only=True)
    tags_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all(), write_only=True, source='tags'
    )

    branch = BranchSerializer(read_only=True)
    branch_id = serializers.PrimaryKeyRelatedField(
        queryset=Branch.objects.all(), write_only=True, source='branch'
    )

    availabilities = AvailabilitySerializer(many=True, read_only=True)

    class Meta:
        model = Space
        fields = [
            'id', 'name', 'description', 'type', 'capacity',
            'price_per_hour', 'price_per_day', 'price_per_month',
            'branch', 'branch_id',
            'amenities', 'amenities_ids',
            'tags', 'tags_ids',
            'max_simultaneous_reservations',
            'latitude', 'longitude',
            'is_available', 'image',
            'rules', 'cancellation_policy', 'notes',
            'access_24_7', 'accessible_for_disabled', 'has_special_equipment',
            'availabilities',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate(self, data):
        # Validar precios
        for price_field in ['price_per_hour', 'price_per_day', 'price_per_month']:
            if price_field in data and data[price_field] is not None and data[price_field] < 0:
                raise serializers.ValidationError({price_field: "El precio no puede ser negativo"})

        # Validar capacidad
        if 'capacity' in data and data['capacity'] <= 0:
            raise serializers.ValidationError({'capacity': "La capacidad debe ser mayor a cero"})

        # Validar latitud y longitud
        lat = data.get('latitude')
        lon = data.get('longitude')
        if lat is not None and (lat < -90 or lat > 90):
            raise serializers.ValidationError({'latitude': "La latitud debe estar entre -90 y 90"})
        if lon is not None and (lon < -180 or lon > 180):
            raise serializers.ValidationError({'longitude': "La longitud debe estar entre -180 y 180"})

        return data
