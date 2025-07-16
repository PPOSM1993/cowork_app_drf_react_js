from django.urls import path
from .views import NotificationListCreateView, NotificationDetailView, NotificationSearchView, MarkAsReadView

urlpatterns = [
    path('notifications/', NotificationListCreateView.as_view(), name='notification-list-create'),
    path('notifications/<int:pk>/', NotificationDetailView.as_view(), name='notification-detail'),
    path('notifications/search/', NotificationSearchView.as_view(), name='notification-search'),
    path('notifications/<int:pk>/mark-as-read/', MarkAsReadView.as_view(), name='mark-notification-as-read'),
]
