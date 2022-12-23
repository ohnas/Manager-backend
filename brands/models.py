from django.db import models
from common.models import CommonModel

# Create your models here.


class Brand(CommonModel):

    name = models.CharField(max_length=150)
    description = models.TextField(null=True)
    user = models.ForeignKey(to="users.User", on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return self.name
