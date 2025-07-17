from django.contrib import admin
from .models import Recommendation

@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'user__email', 'user__first_name', 'user__last_name')
    autocomplete_fields = ('user',)
