import django_filters

from .models import AudienceTicket, Sponsor, SponsorRights


class SponsorFilter(django_filters.FilterSet):
    class Meta:
        model = Sponsor
        fields = ["sponsor_type", "sponsor_name"]


class SponsorRightsFilter(django_filters.FilterSet):
    class Meta:
        model = SponsorRights
        fields = ["sponsor", "event", "rights_type", "rights_status"]


class AudienceTicketFilter(django_filters.FilterSet):
    class Meta:
        model = AudienceTicket
        fields = ["event", "purchase_channel", "refund_status", "notice_confirm_status"]

