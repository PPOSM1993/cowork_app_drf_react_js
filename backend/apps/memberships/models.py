from django.db import models
from django.utils import timezone

class Membership(models.Model):
    PLAN_CHOICES = [
        ('basic', 'Basic'),
        ('standard', 'Standard'),
        ('premium', 'Premium'),
        ('custom', 'Custom'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired'),
    ]

    customer = models.ForeignKey('customers.Customer', on_delete=models.CASCADE, related_name='memberships')
    plan = models.CharField(max_length=50, choices=PLAN_CHOICES, default='basic')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    is_active = models.BooleanField(default=True)  # <--- agrega este campo

    auto_renew = models.BooleanField(default=True)
    usage_limit = models.PositiveIntegerField(default=0, help_text="Cantidad de usos incluidos en el plan")
    usage_count = models.PositiveIntegerField(default=0, help_text="Cantidad de usos realizados")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_currently_active(self):
        return self.status == 'active' and (self.end_date is None or self.end_date >= timezone.now())

    def __str__(self):
        return f"{self.customer} - {self.plan}"
