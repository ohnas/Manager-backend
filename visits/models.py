from django.db import models
from common.models import CommonModel

# Create your models here.


class Visit(CommonModel):

    num = models.PositiveIntegerField()
    brand = models.ForeignKey(to="brands.Brand", on_delete=models.CASCADE)
    visit_date = models.DateField()

    def __str__(self):
        return f"{self.visit_date}"
