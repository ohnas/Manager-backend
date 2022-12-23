from django.db import models
from common.models import CommonModel

# Create your models here.


class Sale(CommonModel):

    product = models.ForeignKey(
        to="products.Product", on_delete=models.SET_NULL, null=True
    )
    site = models.ForeignKey(to="sites.Site", on_delete=models.SET_NULL, null=True)
    count = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    delivery_price = models.PositiveIntegerField()
    pay_time = models.DateTimeField()
