from django.db import models
from django.conf import settings

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('system', 'System'),
        ('reservation', 'Reservation'),
        ('payment', 'Payment'),
        ('support', 'Support'),
        ('promotion', 'Promotion'),
        ('general', 'General'),
    ]

    DELIVERY_METHODS = [
        ('internal', 'Internal'),
        ('email', 'Email'),
        ('push', 'Push'),
        ('sms', 'SMS'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    title = models.CharField(max_length=255)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='system')
    delivery_method = models.CharField(max_length=20, choices=DELIVERY_METHODS, default='internal')
    is_read = models.BooleanField(default=False)
    sent_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(blank=True, null=True)
    related_object_type = models.CharField(max_length=100, blank=True, null=True)  # Ej: 'Invoice', 'Reservation'
    related_object_id = models.PositiveIntegerField(blank=True, null=True)         # ID relacionado

    def mark_as_read(self):
        if not self.is_read:
            self.is_read = True
            from django.utils.timezone import now
            self.read_at = now()
            self.save()

    class Meta:
        ordering = ['-sent_at']

    def __str__(self):
        return f'{self.title} -> {self.user.email}'
