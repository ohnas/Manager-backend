from django.db import models
from common.models import CommonModel

# Create your models here.


class Site(CommonModel):
    class SiteKindChoices(models.TextChoices):
        SALE = ("sale_site", "Sale")
        ADVERTISING = ("advertising_site", "Advertising")

    name = models.CharField(max_length=150)
    url = models.URLField(null=True, blank=True)
    brand = models.ForeignKey(to="brands.Brand", on_delete=models.CASCADE)
    api_key = models.CharField(max_length=150, null=True, blank=True)
    secret_key = models.CharField(max_length=150, null=True, blank=True)
    ad_account_id = models.CharField(max_length=150, null=True, blank=True)
    kind = models.CharField(max_length=20, choices=SiteKindChoices.choices, null=True)

    def __str__(self) -> str:
        return self.name
