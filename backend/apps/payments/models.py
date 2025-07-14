from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.customers.models import Customer
from apps.reservations.models import Reservation

class Payment(models.Model):
    class PaymentMethod(models.TextChoices):
        CREDIT_CARD = 'credit_card', _('Tarjeta de Crédito')
        DEBIT_CARD = 'debit_card', _('Tarjeta de Débito')
        TRANSFER = 'transfer', _('Transferencia Bancaria')
        CASH = 'cash', _('Efectivo')
        OTHER = 'other', _('Otro')

    class PaymentStatus(models.TextChoices):
        PENDING = 'pending', _('Pendiente')
        PAID = 'paid', _('Pagado')
        FAILED = 'failed', _('Fallido')
        REFUNDED = 'refunded', _('Reembolsado')

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='payments')
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='payments', null=True, blank=True)

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    method = models.CharField(max_length=20, choices=PaymentMethod.choices)
    status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)

    payment_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    @property
    def total_amount(self):
        return (self.amount + self.tax) - self.discount

    def __str__(self):
        return f"{self.customer} - {self.total_amount} ({self.get_status_display()})"
