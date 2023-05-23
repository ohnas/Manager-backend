from django.db import models
from common.models import CommonModel

# Create your models here.


class Brand(CommonModel):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(null=True, blank=True)
    user = models.ForeignKey(to="users.User", on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return self.name


class BrandData(CommonModel):
    brand = models.ForeignKey(to="brands.Brand", on_delete=models.CASCADE)
    imweb_price = models.PositiveIntegerField()
    imweb_deliv_price = models.PositiveIntegerField()
    product_cost = models.PositiveIntegerField()
    product_profit = models.IntegerField()
    facebook_ad_expense_krw = models.FloatField()
    expense = models.FloatField()
    operating_profit = models.FloatField()
    imweb_nomal_order_counter = models.PositiveIntegerField()
    imweb_npay_order_counter = models.PositiveIntegerField()
    imweb_count = models.PositiveIntegerField()
    date = models.DateField()

    def __str__(self) -> str:
        return f"{self.brand.name}'s Data from {self.date}"


class ExpenseByHand(CommonModel):
    brand = models.ForeignKey(to="brands.Brand", on_delete=models.CASCADE)
    description = models.CharField(max_length=150)
    expense_by_hand = models.PositiveIntegerField()
    date = models.DateField()

    def __str__(self) -> str:
        return f"{self.brand.name}'s {self.description} from {self.date}"
