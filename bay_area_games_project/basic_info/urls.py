from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AthleteViewSet, TeamViewSet

router = DefaultRouter()
router.register(r"teams", TeamViewSet)
router.register(r"athletes", AthleteViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
