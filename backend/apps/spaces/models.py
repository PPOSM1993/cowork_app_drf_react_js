from django.db import models

# Tipos de espacio
class SpaceType(models.TextChoices):
    SHARED = 'shared', 'Espacio Compartido'
    PRIVATE = 'private', 'Oficina Privada'
    MEETING_ROOM = 'meeting', 'Sala de Reuniones'
    EVENT_SPACE = 'event', 'Espacio para Eventos'

# Etiquetas para filtrar espacios
class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# Servicios o amenidades que ofrece un espacio
class Amenity(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=100, blank=True, help_text="Icono o clase CSS")

    def __str__(self):
        return self.name

# Sedes o branches (idealmente estaría en app branches, pero aquí por simplicidad)
class Branch(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    image = models.ImageField(upload_to='branches/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.city}"

# Horarios de disponibilidad por día de la semana
class Availability(models.Model):
    DAYS_OF_WEEK = [
        (0, 'Lunes'),
        (1, 'Martes'),
        (2, 'Miércoles'),
        (3, 'Jueves'),
        (4, 'Viernes'),
        (5, 'Sábado'),
        (6, 'Domingo'),
    ]

    space = models.ForeignKey('Space', on_delete=models.CASCADE, related_name='availabilities')
    day_of_week = models.PositiveSmallIntegerField(choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        unique_together = ('space', 'day_of_week', 'start_time', 'end_time')

    def __str__(self):
        return f"{self.space.name} - {self.get_day_of_week_display()} {self.start_time} a {self.end_time}"

# Modelo principal de Espacio
class Space(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    type = models.CharField(max_length=20, choices=SpaceType.choices, default=SpaceType.SHARED)
    capacity = models.PositiveIntegerField(help_text="Máximo de personas")
    price_per_hour = models.DecimalField(max_digits=8, decimal_places=2)
    price_per_day = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    price_per_month = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='spaces')

    amenities = models.ManyToManyField(Amenity, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

    max_simultaneous_reservations = models.PositiveIntegerField(default=1)

    # Ubicación geográfica para mapas
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='spaces/', blank=True, null=True)

    rules = models.TextField(blank=True, null=True, help_text="Reglas o políticas del espacio")
    cancellation_policy = models.TextField(blank=True, null=True, help_text="Política de cancelación")
    notes = models.TextField(blank=True, null=True)

    access_24_7 = models.BooleanField(default=False)
    accessible_for_disabled = models.BooleanField(default=False)
    has_special_equipment = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"
