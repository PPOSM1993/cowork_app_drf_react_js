from rest_framework import serializers
from .models import *

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'name']


class CitySerializer(serializers.ModelSerializer):
    region = RegionSerializer(read_only=True)
    region_id = serializers.PrimaryKeyRelatedField(
        queryset=Region.objects.all(), source='region', write_only=True
    )

    class Meta:
        model = City
        fields = ['id', 'name', 'region', 'region_id']

class BranchSerializer(serializers.ModelSerializer):

    region = RegionSerializer(read_only=True)
    city = CitySerializer(read_only=True)

    region_id = serializers.PrimaryKeyRelatedField(
        queryset=Region.objects.all(), source='region', write_only=True, required=False
    )
    city_id = serializers.PrimaryKeyRelatedField(
        queryset=City.objects.all(), source='city', write_only=True, required=False
    )

    class Meta:
        model = Branch
        fields = [
            'id',
            'name',
            'address',
            'phone',
            'email',
            'image',
            'is_active',
            'opening_hours',
            'latitude',
            'longitude',
            'notes',
            'slug',
            'region',
            'region_id',
            'city',
            'city_id',
            'created_at',
            'updated_at',
        ]

        read_only_fields = ['id', 'slug', 'created_at', 'updated_at']


        def validate_email(self, value):
            # Si estamos editando (PUT/PATCH)
            if self.instance:
                # Excluir al cliente actual en la verificación de email único
                if Branch.objects.exclude(pk=self.instance.pk).filter(email=value).exists():
                    raise serializers.ValidationError("Este correo ya existe.")
            else:
                # Si es creación (POST)
                if Branch.objects.filter(email=value).exists():
                    raise serializers.ValidationError("Este correo ya existe.")
            return value


        def validate(self, data):
            if data['name'] == '':
                raise serializers.ValidationError('Branch name is required')
            elif data['address'] == '':
                raise serializers.ValidationError('Branch address is required')
            elif data['city'] == '':
                raise serializers.ValidationError('Branch city is required')
            elif data['region'] == '':
                raise serializers.ValidationError('Branch region is required')
            elif data['phone'] == '':
                raise serializers.ValidationError('Branch phone is required')
            elif data['email'] == '':
                raise serializers.ValidationError('Branch email is required')
        
            return data
    