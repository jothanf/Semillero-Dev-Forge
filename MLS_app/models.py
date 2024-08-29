from django.db import models
from user_app.models import UserCustomerModel

# Create your models here.
class PropertyModel(models.Model):
    owner = models.ForeignKey(UserCustomerModel, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    area = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.address} - {self.price}"