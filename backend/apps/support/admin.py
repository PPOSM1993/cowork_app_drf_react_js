
from django.contrib import admin
from .models import SupportTicket

@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'status', 'priority', 'created_by', 'assigned_to', 'created_at')
    list_filter = ('status', 'priority', 'created_at')
    search_fields = ('title', 'description', 'created_by__email', 'assigned_to__email')
    raw_id_fields = ('created_by', 'assigned_to')  # Corrección aquí
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
