from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
from django.utils.text import slugify

# Create your models here.

phone_regex = RegexValidator(
    regex=r'^(\+56)?\s?9\d{8}$',
    message="Ingrese un número de teléfono válido. Ejemplo: +56912345678 o 912345678."
)

# Región (Ej: Región Metropolitana)
class Region(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Ciudad (Ej: Santiago)
class City(models.Model):
    name = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='cities')

    def __str__(self):
        return self.name


class Branch(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    # Ubicación geográfica
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    phone = models.CharField("Phone", validators=[phone_regex], max_length=17, blank=True, unique=True)
    email = models.EmailField(blank=True)
    image = models.ImageField(upload_to='branches/', blank=True, null=True)

    is_active = models.BooleanField(default=True)
    #manager = models.ForeignKey('employees.Employee', on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_branches')
    #manager quedara pendiente hasta crear la app de Employee
    opening_hours = models.CharField(max_length=255, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    notes = models.TextField(blank=True)
    slug = models.SlugField(unique=True, blank=True)

    # Campo de fecha de creación correctamente definido
    created_at = models.DateTimeField("Created at", default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name}-{self.city}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.city}"