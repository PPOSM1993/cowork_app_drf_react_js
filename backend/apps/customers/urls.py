from django.urls import path
from .views import (
    CustomerListCreateView,
    CustomerRetrieveUpdateDestroyView,
    SearchCustomer,
    DeleteCustomer,
    CustomerDetail
)

urlpatterns = [
    # CRUD básico con vistas basadas en clases
    path('', CustomerListCreateView.as_view(), name='customer-list-create'),
    path('<int:pk>/', CustomerRetrieveUpdateDestroyView.as_view(), name='customer-detail'),

    # Vistas basadas en funciones
    path('search/', SearchCustomer, name='customer-search'),
    path('delete/<int:pk>/', DeleteCustomer, name='customer-delete'),
    path('detail/<int:pk>/', CustomerDetail, name='customer-detail-func'),
]
