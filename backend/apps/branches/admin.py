from django.contrib import admin
from .models import Branch

@admin.register(Branch)
class BranchsAdmin(admin.ModelAdmin):
    pass