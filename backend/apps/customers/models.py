from django.db import models
from django.core.validators import RegexValidator, EmailValidator

# ----------------------
# Región
# ----------------------
class Region(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# ----------------------
# Ciudad
# ----------------------
class City(models.Model):
    name = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='cities')

    def __str__(self):
        return self.name


# ----------------------
# Customer
# ----------------------
class Customer(models.Model):
    CUSTOMER_TYPE_CHOICES = [
        ('individual', 'Persona Natural'),
        ('company', 'Empresa'),
    ]

    customer_type = models.CharField(max_length=20, choices=CUSTOMER_TYPE_CHOICES, default='individual')

    # Datos generales
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)

    tax_id = models.CharField(max_length=50, unique=True)
    business_activity = models.CharField(max_length=255, blank=True, null=True)

    # Contacto con validaciones
    email = models.CharField(
        max_length=254,
        blank=True,
        null=True,
        validators=[EmailValidator(message="Ingrese un correo electrónico válido.")]
    )

    phone_regex = RegexValidator(
        regex=r'^\+?56\d{9}$',  # +569XXXXXXXX
        message="El número debe tener el formato: +569XXXXXXXX."
    )
    phone = models.CharField(
        validators=[phone_regex],
        max_length=15,
        blank=True,
        null=True
    )

    address = models.TextField(blank=True, null=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    country = models.CharField(max_length=100, default='Chile')

    website = models.URLField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.company_name if self.customer_type == 'company' else f"{self.first_name} {self.last_name}"
