from django.contrib import admin
from .models import APIKey, APIAccessLog

@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'key', 'is_active', 'usage_limit_per_day', 'created_at', 'expires_at')
    list_filter = ('is_active', 'created_at', 'expires_at')
    search_fields = ('name', 'user__email', 'key')
    readonly_fields = ('key', 'created_at')
    ordering = ('-created_at',)
    fieldsets = (
        (None, {
            'fields': ('name', 'user', 'key', 'is_active', 'usage_limit_per_day')
        }),
        ('Fechas', {
            'fields': ('created_at', 'expires_at')
        }),
    )


@admin.register(APIAccessLog)
class APIAccessLogAdmin(admin.ModelAdmin):
    list_display = ('api_key', 'endpoint', 'method', 'timestamp', 'success', 'response_code', 'ip_address')
    list_filter = ('success', 'method', 'timestamp')
    search_fields = ('api_key__key', 'endpoint', 'ip_address')
    readonly_fields = ('api_key', 'endpoint', 'method', 'timestamp', 'success', 'response_code', 'ip_address')
    ordering = ('-timestamp',)
