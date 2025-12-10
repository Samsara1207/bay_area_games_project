from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import DataReportViewSet

router = DefaultRouter()
router.register(r"data-reports", DataReportViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
