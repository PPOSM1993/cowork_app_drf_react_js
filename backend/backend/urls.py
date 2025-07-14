from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/authentication/', include('apps.authentication.urls')),
    path('api/branches/', include('apps.branches.urls')),
    path('api/spaces/', include('apps.spaces.urls')),
    path('api/customers/', include('apps.customers.urls')),
    path('api/reservations/', include('apps.reservations.urls')),
    path('api/payments/', include('apps.payments.urls')),
    path('api/memberships/', include('apps.memberships.urls')),
]
