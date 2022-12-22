from django.db import models
from common.models import CommonModel

# Create your models here.


class Site(CommonModel):

    name = models.CharField(max_length=150)
    url = models.URLField()
    brand = models.ForeignKey(to="brands.Brand", on_delete=models.CASCADE)
