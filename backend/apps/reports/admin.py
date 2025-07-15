from django.contrib import admin
from .models import Report

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'report_type', 'created_by', 'generated_at', 'is_active')
    list_filter = ('report_type', 'is_active', 'generated_at')
    search_fields = ('title', 'description', 'created_by__email')
    readonly_fields = ('generated_at', 'last_modified')
    ordering = ('-generated_at',)

    fieldsets = (
        ('Detalles Generales', {
            'fields': ('title', 'description', 'report_type', 'data', 'observations')
        }),
        ('Estado y Gestión', {
            'fields': ('is_active', 'created_by', 'generated_at', 'last_modified')
        }),
    )
