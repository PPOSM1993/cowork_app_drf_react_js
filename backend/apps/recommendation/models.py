from django.db import models
from django.conf import settings

class Recommendation(models.Model):
    RECOMMENDATION_TYPES = [
        ('space', 'Space'),
        ('service', 'Service'),
        ('promotion', 'Promotion'),
        ('custom', 'Custom'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='recommendations'
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    recommendation_type = models.CharField(max_length=20, choices=RECOMMENDATION_TYPES, default='custom')
    related_object_id = models.PositiveIntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    priority = models.PositiveIntegerField(default=1, help_text="Prioridad de la recomendación, 1 es la más alta.")
    clicks = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['priority', '-created_at']

    def increment_clicks(self):
        self.clicks += 1
        self.save(update_fields=['clicks'])

    def increment_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def __str__(self):
        return f'{self.title} -> {self.user.email}'
