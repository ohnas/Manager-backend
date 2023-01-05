from rest_framework.serializers import ModelSerializer
from advertisings.models import Advertising
from sites.serializers import SiteSerializer


class AdvertisingSerializer(ModelSerializer):

    site = SiteSerializer(read_only=True)

    class Meta:
        model = Advertising
        fields = (
            "site",
            "campaign_name",
            "reach",
            "impressions",
            "frequency",
            "spend",
            "cpm",
            "purchase_roas",
            "website_ctr",
            "cost_per_unique_inline_link_click",
            "purchase",
            "landing_page_view",
            "link_click",
            "ad_date",
        )
