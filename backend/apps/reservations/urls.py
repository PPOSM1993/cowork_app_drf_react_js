from django.urls import path
from .views import (
    ReservationListCreateView,
    ReservationRetrieveUpdateDestroyView,
    ReservationsByCustomer
)

urlpatterns = [
    path('', ReservationListCreateView.as_view(), name='reservation-list-create'),
    path('<int:pk>/', ReservationRetrieveUpdateDestroyView.as_view(), name='reservation-detail'),
    path('customer/<int:customer_id>/', ReservationsByCustomer, name='reservations-by-customer'),
]
