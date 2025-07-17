from django.contrib import admin
from .models import IdentityVerification

@admin.register(IdentityVerification)
class IdentityVerificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'document_type', 'document_number', 'status', 'submitted_at', 'reviewed_at')
    list_filter = ('document_type', 'status', 'submitted_at')
    search_fields = ('user__email', 'document_number')
    readonly_fields = ('submitted_at', 'reviewed_at')

    fieldsets = (
        (None, {
            'fields': ('user', 'document_type', 'document_number')
        }),
        ('Imágenes del documento', {
            'fields': ('document_front_image', 'document_back_image', 'selfie_image')
        }),
        ('Estado de verificación', {
            'fields': ('status', 'review_comments', 'submitted_at', 'reviewed_at')
        }),
    )
