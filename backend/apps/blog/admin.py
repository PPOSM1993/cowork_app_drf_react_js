from django.contrib import admin
from .models import BlogPost

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_at', 'is_published')
    list_filter = ('is_published', 'published_at', 'author')
    search_fields = ('title', 'content', 'author__email')
    ordering = ('-published_at',)
    readonly_fields = ('published_at', 'updated_at')
