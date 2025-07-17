from django.contrib import admin
from .models import Employee

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'rut',
        'email',
        'phone',
        'role',
        'is_active',
        'date_joined',
    )
    list_filter = ('is_active', 'role')
    search_fields = ('first_name', 'last_name', 'rut', 'email', 'phone')
    ordering = ('last_name', 'first_name')
    readonly_fields = ('date_joined', 'updated_at')
