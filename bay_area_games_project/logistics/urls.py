from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import LogisticsDetailViewSet, SupplierViewSet, VolunteerViewSet

router = DefaultRouter()
router.register(r"suppliers", SupplierViewSet)
router.register(r"logistics-details", LogisticsDetailViewSet)
router.register(r"volunteers", VolunteerViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
