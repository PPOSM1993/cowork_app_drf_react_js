from django.db import models
import re
from django.core.exceptions import ValidationError

def validate_rut(value):
    rut_pattern = r'^\d{1,2}\.\d{3}\.\d{3}-[\dkK]$'
    if not re.match(rut_pattern, value):
        raise ValidationError('RUT inválido. Formato esperado: XX.XXX.XXX-X')

def validate_phone(value):
    phone_pattern = r'^\+?56\d{9}$'
    if not re.match(phone_pattern, value):
        raise ValidationError('Teléfono inválido. Debe incluir +56 y 9 dígitos.')

class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    rut = models.CharField(max_length=15, unique=True, validators=[validate_rut])
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, validators=[validate_phone])
    birth_date = models.DateField()
    role = models.CharField(max_length=100, help_text='Cargo o función del empleado')
    is_active = models.BooleanField(default=True)
    date_joined = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.role})'
