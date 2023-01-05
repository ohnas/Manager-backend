from django.db import models
from common.models import CommonModel


class Advertising(CommonModel):

    site = models.ForeignKey(to="sites.Site", on_delete=models.SET_NULL, null=True)
    campaign_id = models.CharField(max_length=150)
    campaign_name = models.CharField(max_length=150)
    reach = models.CharField(max_length=150)
    impressions = models.CharField(max_length=150)
    frequency = models.CharField(max_length=150)
    spend = models.CharField(max_length=150)
    cpm = models.CharField(max_length=150)
    purchase_roas = models.CharField(max_length=150)
    website_ctr = models.CharField(max_length=150)
    cost_per_unique_inline_link_click = models.CharField(max_length=150)
    purchase = models.CharField(max_length=150)
    landing_page_view = models.CharField(max_length=150)
    link_click = models.CharField(max_length=150)
    ad_date = models.DateField()

    def __str__(self) -> str:
        return self.campaign_name
