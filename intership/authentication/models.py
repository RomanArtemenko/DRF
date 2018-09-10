from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=12, blank=False)
    social_id = models.CharField(max_length= 128, blank=True)
    nickname = models.CharField(max_length=50)
