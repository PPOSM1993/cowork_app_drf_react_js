from django.urls import path
from .views import AdvancedAnalyticsDashboardView

urlpatterns = [
    path('dashboard/', AdvancedAnalyticsDashboardView.as_view(), name='analytics-dashboard'),
]
