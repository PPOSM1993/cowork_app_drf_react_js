from django.urls import path
from .views import *

urlpatterns = [
    # Spaces
    path('', SpaceListCreateView.as_view(), name='space-list-create'),
    path('spaces/<int:pk>/', SpaceRetrieveUpdateDestroyView.as_view(), name='space-detail'),

    # Availability
    path('spaces/<int:pk>/availability/', AvailabilityCreateView.as_view(), name='space-availability'),

    # Extras
    path('amenities/', AmenityListView.as_view(), name='amenity-list'),
    path('tags/', TagListView.as_view(), name='tag-list'),
    path('branches/', BranchListView.as_view(), name='branch-list'),
]
