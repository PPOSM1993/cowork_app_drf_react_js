from django.urls import path
from .views import MembershipListCreateView, MembershipRetrieveUpdateDestroyView, MembershipPublicListView

urlpatterns = [
    path('', MembershipListCreateView.as_view(), name='membership-list-create'),
    path('memberships/<int:pk>/', MembershipRetrieveUpdateDestroyView.as_view(), name='membership-detail'),
    path('meberships/public/', MembershipPublicListView.as_view(), name='membership-public-list'),

]
