from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AudienceTicketViewSet, SponsorRightsViewSet, SponsorViewSet

router = DefaultRouter()
router.register(r"sponsors", SponsorViewSet)
router.register(r"sponsor-rights", SponsorRightsViewSet)
router.register(r"audience-tickets", AudienceTicketViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
