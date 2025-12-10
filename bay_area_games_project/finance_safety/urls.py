from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import EpidemicSafetyViewSet, FinanceViewSet

router = DefaultRouter()
router.register(r"finances", FinanceViewSet)
router.register(r"epidemic-safety", EpidemicSafetyViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
