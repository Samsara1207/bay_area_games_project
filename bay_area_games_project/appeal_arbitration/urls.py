from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AppealArbitrationViewSet, AppealViewSet, ArbitrationCommitteeViewSet

router = DefaultRouter()
router.register(r"appeals", AppealViewSet)
router.register(r"arbitration-committees", ArbitrationCommitteeViewSet)
router.register(r"appeal-arbitrations", AppealArbitrationViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
