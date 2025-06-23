from django.db import models
from django.core.validators import RegexValidator

# Create your models here.

phone_regex = RegexValidator(
    regex=r'^(\+56)?\s?9\d{8}$',
    message="Ingrese un número de teléfono válido. Ejemplo: +56912345678 o 912345678."
)

class Branch(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    phone = models.CharField("Phone", validators=[phone_regex], max_length=17, blank=True, unique=True)
    email = models.EmailField(blank=True)
    image = models.ImageField(upload_to='branches/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.city}"
