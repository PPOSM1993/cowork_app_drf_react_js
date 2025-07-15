from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm

User = get_user_model()

class Invoice(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Borrador'),
        ('issued', 'Emitida'),
        ('paid', 'Pagada'),
        ('cancelled', 'Cancelada'),
        ('overdue', 'Vencida'),
    ]

    number = models.CharField(max_length=50, unique=True, blank=True)
    customer = models.ForeignKey('customers.Customer', on_delete=models.CASCADE, related_name='invoices')

    billing_address = models.TextField(blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    purchase_order_reference = models.CharField(max_length=100, blank=True, null=True)

    currency = models.CharField(max_length=5, default='CLP')
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=4, default=1)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    issued_date = models.DateField(default=timezone.now)
    due_date = models.DateField(blank=True, null=True)

    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    sent_to_customer = models.BooleanField(default=False)
    pdf_file = models.FileField(upload_to='invoices/pdfs/', blank=True, null=True)

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Factura #{self.number or "Sin Número"}'

    def calculate_totals(self):
        subtotal = sum(item.total for item in self.items.all())
        tax = subtotal * 0.19  # Asumiendo IVA 19% Chile
        total = subtotal + tax

        self.subtotal = subtotal
        self.tax = tax
        self.total = total

    def save(self, *args, **kwargs):
        if not self.number:
            last_invoice = Invoice.objects.order_by('-id').first()
            next_number = f'F-{timezone.now().year}-{(last_invoice.id + 1) if last_invoice else 1:04d}'
            self.number = next_number

        self.calculate_totals()
        super().save(*args, **kwargs)

    def generate_pdf(self):
        """Genera un PDF básico para la factura"""
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        p.setFont("Helvetica-Bold", 16)
        p.drawString(20 * mm, height - 30 * mm, f"Factura N° {self.number}")

        p.setFont("Helvetica", 12)
        p.drawString(20 * mm, height - 40 * mm, f"Cliente: {str(self.customer)}")
        p.drawString(20 * mm, height - 50 * mm, f"Fecha Emisión: {self.issued_date}")
        p.drawString(20 * mm, height - 60 * mm, f"Fecha Vencimiento: {self.due_date}")
        p.drawString(20 * mm, height - 70 * mm, f"Referencia OC: {self.purchase_order_reference or 'N/A'}")

        p.drawString(20 * mm, height - 90 * mm, f"Total a Pagar: ${self.total}")

        p.setFont("Helvetica-Oblique", 10)
        p.drawString(20 * mm, 20 * mm, f"Generado automáticamente por el sistema.")

        p.showPage()
        p.save()
        buffer.seek(0)
        return buffer


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    description = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        self.total = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.description} - {self.quantity} x {self.unit_price}'
