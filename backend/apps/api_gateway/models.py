from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class APIKey(models.Model):
    key = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='api_keys')
    name = models.CharField(max_length=255, help_text='Nombre descriptivo de la API Key')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    usage_limit_per_day = models.PositiveIntegerField(default=1000, help_text='Límite de peticiones diarias')

    def __str__(self):
        return f'{self.name} ({self.user.email}) - {"Activo" if self.is_active else "Inactivo"}'


class APIAccessLog(models.Model):
    api_key = models.ForeignKey(APIKey, on_delete=models.CASCADE, related_name='access_logs')
    endpoint = models.CharField(max_length=255)
    method = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=True)
    response_code = models.PositiveIntegerField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        ordering = ['-timestamp']
