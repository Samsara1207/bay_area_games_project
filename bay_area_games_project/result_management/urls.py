from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import MedalHonorViewSet, ResultViewSet

router = DefaultRouter()
router.register(r"results", ResultViewSet)
router.register(r"medal-honors", MedalHonorViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
