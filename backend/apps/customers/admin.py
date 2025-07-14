from django.contrib import admin
from .models import Customer, Region, City


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'region')
    search_fields = ('name',)
    list_filter = ('region',)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_name', 'customer_type', 'tax_id', 'phone', 'email', 'region', 'city', 'is_active')
    list_filter = ('customer_type', 'region', 'city', 'is_active')
    search_fields = ('first_name', 'last_name', 'company_name', 'tax_id', 'email', 'phone')
    ordering = ('-created_at',)

    def get_name(self, obj):
        return obj.company_name if obj.customer_type == 'company' else f"{obj.first_name} {obj.last_name}"
    get_name.short_description = 'Nombre / Empresa'
