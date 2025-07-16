from django.urls import path
from .views import (
    SupportTicketListCreateView,
    SupportTicketDetailView,
    MyAssignedTicketsView,
    SearchSupportTicketsView,
    ChangeTicketStatusView
)

urlpatterns = [
    path('tickets/', SupportTicketListCreateView.as_view(), name='support-ticket-list-create'),
    path('tickets/<int:pk>/', SupportTicketDetailView.as_view(), name='support-ticket-detail'),
    path('tickets/my-assigned/', MyAssignedTicketsView.as_view(), name='my-assigned-tickets'),
    path('tickets/search/', SearchSupportTicketsView.as_view(), name='support-ticket-search'),
    path('tickets/<int:pk>/change-status/', ChangeTicketStatusView.as_view(), name='change-ticket-status'),
]
