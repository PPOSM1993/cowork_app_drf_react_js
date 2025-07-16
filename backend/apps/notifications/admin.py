from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'notification_type', 'delivery_method', 'is_read', 'sent_at')
    list_filter = ('notification_type', 'delivery_method', 'is_read', 'sent_at')
    search_fields = ('title', 'message', 'user__email')
    readonly_fields = ('sent_at', 'read_at')
