from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IdentityVerificationViewSet

router = DefaultRouter()
router.register(r'', IdentityVerificationViewSet, basename='identity-verification')

urlpatterns = [
    path('', include(router.urls)),
]
