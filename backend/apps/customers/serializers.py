# apps/customers/serializers.py
from rest_framework import serializers
from .models import Region, City, Customer
import re

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'

class CitySerializer(serializers.ModelSerializer):
    region = RegionSerializer(read_only=True)

    class Meta:
        model = City
        fields = '__all__'


EMAIL_REGEX = r'^[\w\.-]+@[\w\.-]+\.\w+$'
PHONE_REGEX = r'^\+?\d{9,15}$'  # Teléfonos internacionales

class CustomerSerializer(serializers.ModelSerializer):
    region_name = serializers.CharField(source='region.name', read_only=True)
    city_name = serializers.CharField(source='city.name', read_only=True)

    class Meta:
        model = Customer
        fields = [
            'id', 'first_name', 'last_name', 'tax_id',
            'email', 'phone', 'address',
            'region', 'region_name', 'city', 'city_name', 'customer_type',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate_email(self, value):
        value = value.lower().strip()
        if not re.match(EMAIL_REGEX, value):
            raise serializers.ValidationError("Ingrese un email válido.")
        return value

    def validate_phone(self, value):
        value = value.strip()
        if not re.match(PHONE_REGEX, value):
            raise serializers.ValidationError("Ingrese un teléfono válido (ej: +56912345678).")
        return value

    def validate(self, attrs):
        customer_type = attrs.get('customer_type')
        tax_id = attrs.get('tax_id')

        if customer_type == 'EMPRESA' and not tax_id:
            raise serializers.ValidationError({"tax_id": "El RUT es obligatorio para empresas."})

        return attrs