from rest_framework import serializers
from .models import Employee
import re

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

    def validate_rut(self, value):
        rut_pattern = r'^\d{1,2}\.\d{3}\.\d{3}-[\dkK]$'
        if not re.match(rut_pattern, value):
            raise serializers.ValidationError('RUT inválido. Formato esperado: XX.XXX.XXX-X')
        return value

    def validate_phone(self, value):
        phone_pattern = r'^\+?56\d{9}$'
        if not re.match(phone_pattern, value):
            raise serializers.ValidationError('Teléfono inválido. Debe incluir +56 y 9 dígitos.')
        return value

    def validate_email(self, value):
        value = value.lower()
        if Employee.objects.filter(email=value).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError('Ya existe un empleado con este correo.')
        return value

    def validate_rut(self, value):
        # Sobrescribo para validar unicidad manual (evita duplicados en update)
        rut_pattern = r'^\d{1,2}\.\d{3}\.\d{3}-[\dkK]$'
        if not re.match(rut_pattern, value):
            raise serializers.ValidationError('RUT inválido. Formato esperado: XX.XXX.XXX-X')
        if Employee.objects.filter(rut=value).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError('Ya existe un empleado con este RUT.')
        return value

    def validate_birth_date(self, value):
        from datetime import date
        if value >= date.today():
            raise serializers.ValidationError('La fecha de nacimiento debe ser anterior a hoy.')
        return value
