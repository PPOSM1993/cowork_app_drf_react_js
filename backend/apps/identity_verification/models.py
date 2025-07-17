from django.db import models
from django.conf import settings

class IdentityVerification(models.Model):
    DOCUMENT_TYPES = [
        ('dni', 'DNI'),
        ('passport', 'Pasaporte'),
        ('license', 'Licencia de Conducir'),
        ('other', 'Otro'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('approved', 'Aprobado'),
        ('rejected', 'Rechazado'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='verifications')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    document_number = models.CharField(max_length=50)
    document_front_image = models.ImageField(upload_to='id_verifications/fronts/')
    document_back_image = models.ImageField(upload_to='id_verifications/backs/', blank=True, null=True)
    selfie_image = models.ImageField(upload_to='id_verifications/selfies/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(blank=True, null=True)
    review_comments = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('document_type', 'document_number')

    def __str__(self):
        return f'{self.user.email} - {self.document_type} ({self.status})'
