from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import EventOperationViewSet, ScheduleViewSet

router = DefaultRouter()
router.register(r"schedules", ScheduleViewSet)
router.register(r"event-operations", EventOperationViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
