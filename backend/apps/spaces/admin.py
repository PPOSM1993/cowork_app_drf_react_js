from django.contrib import admin
from .models import Space, Amenity, Tag, Branch, Availability
from apps.reviews.admin import ReviewInline
from django.contrib.contenttypes.admin import GenericStackedInline

@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon')
    search_fields = ('name',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

"""@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'region', 'phone', 'email')
    search_fields = ('name', 'city', 'region')
"""
@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ('space', 'day_of_week', 'start_time', 'end_time')
    list_filter = ('day_of_week',)
    search_fields = ('space__name',)

@admin.register(Space)
class SpaceAdmin(admin.ModelAdmin):
    inlines = [ReviewInline]
    list_display = ('name', 'type', 'capacity', 'price_per_hour', 'is_available', 'branch')
    list_filter = ('type', 'is_available', 'branch')
    search_fields = ('name', 'description')
    filter_horizontal = ('amenities', 'tags')
