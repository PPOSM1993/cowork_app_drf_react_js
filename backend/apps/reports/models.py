from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

class Report(models.Model):
    REPORT_TYPE_CHOICES = [
        ('daily', 'Diario'),
        ('weekly', 'Semanal'),
        ('monthly', 'Mensual'),
        ('custom', 'Personalizado'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPE_CHOICES, default='custom')
    generated_at = models.DateTimeField(auto_now_add=True)
    data = models.TextField(help_text="Datos en formato JSON o texto estructurado.")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='reports')
    is_active = models.BooleanField(default=True)
    observations = models.TextField(blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-generated_at']
        verbose_name = 'Reporte'
        verbose_name_plural = 'Reportes'

    def __str__(self):
        return f"{self.title} ({self.get_report_type_display()})"

    def deactivate(self):
        """Desactiva el reporte sin eliminarlo físicamente."""
        self.is_active = False
        self.save()

    def generate_summary(self):
        """Retorna las primeras líneas del contenido como resumen."""
        return self.data[:200] + "..." if len(self.data) > 200 else self.data
