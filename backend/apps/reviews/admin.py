from django.contrib import admin
from .models import Review
from django.contrib.contenttypes.admin import GenericTabularInline

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'content_object', 'rating', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'rating', 'created_at')
    search_fields = ('user__email', 'comment')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')


class ReviewInline(GenericTabularInline):
    model = Review
    extra = 0
    readonly_fields = ('user', 'rating', 'comment', 'created_at')
    can_delete = False
