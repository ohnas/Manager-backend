from django.db import models
from common.models import CommonModel

# Create your models here.


class Product(CommonModel):

    name = models.CharField(max_length=200)
    price = models.PositiveIntegerField()
    brand = models.ForeignKey(to="brands.Brand", on_delete=models.CASCADE)
