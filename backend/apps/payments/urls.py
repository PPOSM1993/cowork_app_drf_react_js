from django.urls import path
from .views import (
    PaymentListCreateView,
    PaymentRetrieveUpdateDestroyView,
    PaymentsByCustomer,
    SearchPayments,
)

urlpatterns = [
    path('', PaymentListCreateView.as_view(), name='payment-list-create'),
    path('<int:pk>/', PaymentRetrieveUpdateDestroyView.as_view(), name='payment-detail'),
    path('customer/<int:customer_id>/', PaymentsByCustomer, name='payments-by-customer'),
    path('search/', SearchPayments, name='payment-search'),
]
