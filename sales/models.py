from django.db import models
from common.models import CommonModel

# Create your models here.


class Brand(CommonModel):

    name = models.CharField(max_length=150)
    description = models.TextField(null=True)
    user = models.ForeignKey(to="users.User", on_delete=models.SET_NULL, null=True)


class Site(CommonModel):

    name = models.CharField(max_length=150)
    url = models.URLField()
    brand = models.ForeignKey(to="sales.Brand", on_delete=models.CASCADE)


class Product(CommonModel):

    name = models.CharField(max_length=200)
    price = models.PositiveIntegerField()
    brand = models.ForeignKey(to="sales.Brand", on_delete=models.CASCADE)
