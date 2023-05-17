from django.db import models
from common.models import CommonModel

# Create your models here.


class Brand(CommonModel):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(null=True, blank=True)
    user = models.ForeignKey(to="users.User", on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return self.name


class Data(CommonModel):
    brand = models.ForeignKey(to="brands.Brand", on_delete=models.CASCADE)
    imweb_price = models.IntegerField()
    imweb_deliv_price = models.IntegerField()
    product_cost = models.IntegerField()
    product_profit = models.IntegerField()
    facebook_ad_expense_krw = models.IntegerField()
    expense = models.IntegerField()
    operating_profit = models.IntegerField()
    date = models.DateField()

    def __str__(self) -> str:
        return f"{self.brand.name}'s Data from {self.date}"
