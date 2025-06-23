from django.urls import path
from .views import *

urlpatterns = [
    # Spaces
    path('', BranchesListAPIView.as_view(), name='branches-list-create'),
    path('create/', CreateBranchesAPIView.as_view(), name='create-branches'),
    path('delete/<int:pk>/', DeleteBranches, name='delete-branches'),
    path('delete/<int:pk>/', DeleteBranches, name='delete-branch'),
    path('search/', SearchBranch, name='search-branch'),
]
