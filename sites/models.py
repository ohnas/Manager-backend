from django.db import models
from common.models import CommonModel

# Create your models here.


class Site(CommonModel):

    name = models.CharField(max_length=150)
    url = models.URLField()
    brand = models.ForeignKey(to="brands.Brand", on_delete=models.CASCADE)
    api_key = models.CharField(max_length=150, null=True, blank=True)
    secret_key = models.CharField(max_length=150, null=True, blank=True)
    ad_account_id = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self) -> str:
        return self.name
