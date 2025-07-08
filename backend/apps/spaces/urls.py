from django.urls import path
from .views import *

urlpatterns = [
    # -------------------------
    # SPACES
    # -------------------------
    path('', SpaceListCreateView.as_view(), name='space-list-create'),
    path('spaces/<int:pk>/', SpaceRetrieveUpdateDestroyView.as_view(), name='space-detail'),
    path('spaces/branch/<int:branch_id>/', SpacesByBranchView.as_view(), name='spaces-by-branch'),
    path('public/', SpacePublicListView.as_view(), name='public-space-list'),

    # -------------------------
    # AVAILABILITY
    # -------------------------
    path('availability/create/', AvailabilityCreateView.as_view(), name='availability-create'),
    path('availability/space/<int:space_id>/', AvailabilityListBySpaceView.as_view(), name='availability-by-space'),
    path('availability/<int:pk>/', AvailabilityUpdateDeleteView.as_view(), name='availability-update-delete'),

    # -------------------------
    # AMENITIES
    # -------------------------
    path('amenities/', AmenityListView.as_view(), name='amenity-list'),
    path('amenities/create/', AmenityCreateView.as_view(), name='amenity-create'),

    # -------------------------
    # TAGS
    # -------------------------
    path('tags/', TagListView.as_view(), name='tag-list'),
    path('tags/create/', TagCreateView.as_view(), name='tag-create'),

    # -------------------------
    # BRANCHES (solo lectura aquí)
    # -------------------------
    path('branches/', BranchListView.as_view(), name='branch-list'),
]
