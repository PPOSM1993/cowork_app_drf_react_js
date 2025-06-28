from django.urls import path
from .views import (
    BranchesListAPIView,
    CreateBranchesAPIView,
    DeleteBranches,
    BranchesDetail,
    SearchBranch,
)

urlpatterns = [
    # 🔍 Listar todas las sucursales
    path('', BranchesListAPIView.as_view(), name='branches-list-create'),
    # ➕ Crear una nueva sucursal
    path('create/', CreateBranchesAPIView.as_view(), name='create-branches'),
    # ✏️ Obtener/Editar detalle de una sucursal por ID
    path('edit/<int:pk>/', BranchesDetail, name='edit-branch'),
    # ❌ Eliminar una sucursal
    path('delete/<int:pk>/', DeleteBranches, name='delete-branches'),
    # 🔎 Buscar sucursales
    path('search/', SearchBranch, name='search-branch'),
]
