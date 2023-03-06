from django.db import models
from common.models import CommonModel

# Create your models here.


class Event(CommonModel):

    name = models.CharField(max_length=200)
    brand = models.ForeignKey(to="brands.Brand", on_delete=models.CASCADE)
    product = models.ForeignKey(to="products.Product", on_delete=models.CASCADE)
    event_date = models.DateField()

    def __str__(self) -> str:
        return self.name
