from django.urls import path
from .views import (
    ReportListCreateView,
    ReportDetailView,
    ReportSearchView,
    GenerateReportView
)

urlpatterns = [
    path('', ReportListCreateView.as_view(), name='report-list-create'),
    path('<int:pk>/', ReportDetailView.as_view(), name='report-detail'),
    path('search/', ReportSearchView.as_view(), name='report-search'),
    path('generate/<int:pk>/', GenerateReportView.as_view(), name='report-generate'),
]
