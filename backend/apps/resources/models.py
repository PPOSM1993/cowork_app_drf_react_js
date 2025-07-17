from django.db import models

class Resource(models.Model):
    RESOURCE_TYPES = [
        ('room', 'Room'),
        ('equipment', 'Equipment'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=255)
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES, default='other')
    description = models.TextField(blank=True, null=True)
    capacity = models.PositiveIntegerField(default=1, help_text='Número máximo de personas o unidades')
    is_available = models.BooleanField(default=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.get_resource_type_display()})"
