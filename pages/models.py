from django.db import models
from common.models import CommonModel

# Create your models here.


class Page(CommonModel):

    view = models.PositiveIntegerField()
    brand = models.ForeignKey(to="brands.Brand", on_delete=models.CASCADE)
    page_date = models.DateField()

    def __str__(self):
        return f"{self.page_date}"
