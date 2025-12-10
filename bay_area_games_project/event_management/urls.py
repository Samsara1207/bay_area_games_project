from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AthleteEventViewSet, EventViewSet, GroupViewSet, VenueViewSet

router = DefaultRouter()
router.register(r"venues", VenueViewSet)
router.register(r"events", EventViewSet)
router.register(r"groups", GroupViewSet)
router.register(r"athlete-events", AthleteEventViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
