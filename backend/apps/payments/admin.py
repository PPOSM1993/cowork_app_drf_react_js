from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'reservation', 'amount', 'discount', 'tax', 'total_amount', 'method', 'status', 'payment_date')
    list_filter = ('method', 'status', 'payment_date')
    search_fields = ('customer__first_name', 'customer__last_name', 'reservation__id')
    readonly_fields = ('payment_date', 'total_amount')
