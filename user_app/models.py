from django.contrib.auth.models import User
from django.db import models

class UserAgentModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=30, unique=True, blank=True)
    phone = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.nickname

class UserCustomerModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    agent = models.ForeignKey(UserAgentModel, on_delete=models.CASCADE, related_name='customers')
    phone = models.CharField(max_length=15)
    owner = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username