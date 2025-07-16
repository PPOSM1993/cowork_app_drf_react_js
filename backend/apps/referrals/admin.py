from django.contrib import admin
from .models import Referral

@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ['referrer', 'referred_email', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['referrer__email', 'referred_email', 'referral_code']
    readonly_fields = ['referral_code', 'created_at', 'updated_at']

    ordering = ['-created_at']
