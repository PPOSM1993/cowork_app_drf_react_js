from django.contrib import admin
from .models import Reservation

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'customer', 'space', 'start_datetime', 'end_datetime',
        'status', 'payment_status', 'payment_method', 'total_price'
    )
    list_filter = (
        'status', 'payment_status', 'payment_method', 'reservation_type',
        'space__branch', 'created_at'
    )
    search_fields = (
        'customer__first_name', 'customer__last_name', 'space__name',
        'billing_reference', 'notes'
    )
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'start_datetime'
    ordering = ('-created_at',)
