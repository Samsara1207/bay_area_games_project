from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import RefereeArrangementViewSet, RefereeGroupViewSet, RefereeViewSet

router = DefaultRouter()
router.register(r"referees", RefereeViewSet)
router.register(r"referee-groups", RefereeGroupViewSet)
router.register(r"referee-arrangements", RefereeArrangementViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
