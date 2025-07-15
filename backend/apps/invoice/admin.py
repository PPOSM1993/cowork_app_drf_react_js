

from django.contrib import admin
from .models import *

class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1
    fields = ['description', 'quantity', 'unit_price', 'total']
    readonly_fields = ['total']

    def has_delete_permission(self, request, obj=None):
        return True


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        'number',
        'customer',
        'issued_date',
        'due_date',
        'total',
        'status',
        'sent_to_customer',
    )
    list_filter = ('status', 'issued_date', 'due_date', 'sent_to_customer')
    search_fields = ('number', 'customer__first_name', 'customer__last_name', 'customer__company_user')
    ordering = ('-issued_date',)

    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Información Principal', {
            'fields': ('number', 'customer', 'purchase_order_reference')
        }),
        ('Fechas', {
            'fields': ('issued_date', 'due_date')
        }),
        ('Estado y Total', {
            'fields': ('total', 'status', 'sent_to_customer')
        }),
        ('Trazabilidad', {
            'fields': ('created_at', 'updated_at')
        }),
    )
