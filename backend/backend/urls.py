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
    path('api/reports/', include('apps.reports.urls')),
    path('api/invoice/', include('apps.invoice.urls')),
    path('api/support/', include('apps.support.urls')),
    path('api/notifications/', include('apps.notifications.urls')),
    path('api/referrals/', include('apps.referrals.urls')),
    path('api/recommendations/', include('apps.recommendation.urls')),
    path('api/blog/', include('apps.blog.urls')),
    path('api/reviews/', include('apps.reviews.urls')),
    path('api/resources/', include('apps.resources.urls')),


]
