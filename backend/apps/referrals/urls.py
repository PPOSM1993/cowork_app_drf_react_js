from django.urls import path
from .views import (
    ReferralListCreateView,
    ReferralDetailView,
    MyActiveReferralsView,
)

urlpatterns = [
    path('referrals/', ReferralListCreateView.as_view(), name='referral-list-create'),
    path('referrals/<int:pk>/', ReferralDetailView.as_view(), name='referral-detail'),
    path('referrals/my-active/', MyActiveReferralsView.as_view(), name='my-active-referrals'),
]
