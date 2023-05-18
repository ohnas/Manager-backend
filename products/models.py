from django.db import models
from common.models import CommonModel

# Create your models here.


class Product(CommonModel):
    name = models.CharField(max_length=200, unique=True)
    brand = models.ForeignKey(to="brands.Brand", on_delete=models.CASCADE)
    price = models.PositiveIntegerField(default=0)
    cost = models.PositiveIntegerField(default=0)
    delivery_price = models.PositiveIntegerField(default=0)
    logistic_fee = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=0)
    gift_quantity = models.PositiveIntegerField(default=0, null=True, blank=True)

    def __str__(self) -> str:
        return self.name


class Options(CommonModel):
    name = models.CharField(max_length=200, unique=True)
    product = models.ForeignKey(to="products.Product", on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    logistic_fee = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    gift_quantity = models.PositiveIntegerField(default=0, null=True, blank=True)

    def __str__(self) -> str:
        return self.name


class ProductData(CommonModel):
    product = models.ForeignKey(to="products.Product", on_delete=models.CASCADE)
    product_quantity = models.PositiveIntegerField()
    product_gift_quantity = models.PositiveIntegerField()
    shipment_quantity = models.PositiveIntegerField()
    date = models.DateField()

    def __str__(self) -> str:
        return f"{self.product.name}'s Data from {self.date}"
