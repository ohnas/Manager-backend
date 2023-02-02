from django.db import models
from common.models import CommonModel

# Create your models here.


class Product(CommonModel):

    name = models.CharField(max_length=200)
    brand = models.ForeignKey(to="brands.Brand", on_delete=models.CASCADE)
    cost = models.PositiveIntegerField(default=0)
    delivery_price = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return self.name


class Options(CommonModel):

    name = models.CharField(max_length=200)
    product = models.ForeignKey(to="products.Product", on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    cost = models.PositiveIntegerField()
    logistic_fee = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    gift_quantity = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name
