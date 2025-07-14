from django.contrib import admin
from .models import Membership

@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'plan', 'status', 'price', 'start_date', 'end_date', 'auto_renew')
    list_filter = ('plan', 'status', 'auto_renew', 'start_date', 'end_date')
    search_fields = ('customer__first_name', 'customer__last_name', 'plan', 'name')
    ordering = ('-start_date',)
    readonly_fields = ('created_at', 'updated_at', 'usage_count')

    fieldsets = (
        (None, {
            'fields': ('customer', 'plan', 'name', 'description', 'price', 'auto_renew', 'status')
        }),
        ('Uso', {
            'fields': ('usage_limit', 'usage_count')
        }),
        ('Fechas', {
            'fields': ('start_date', 'end_date')
        }),
        ('Tiempos de registro', {
            'fields': ('created_at', 'updated_at')
        }),
    )
