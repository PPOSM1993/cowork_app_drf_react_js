from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/authentication/', include('apps.authentication.urls')),
    path('api/branches/', include('apps.branches.urls')),
    path('api/spaces/', include('apps.spaces.urls')),
]
