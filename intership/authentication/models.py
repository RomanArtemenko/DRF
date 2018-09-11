from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import User, AbstractUser


# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=12, blank=False)
    social_id = models.CharField(max_length= 128, blank=True)
    nickname = models.CharField(max_length=50)

# class CustomUser(AbstractUser):
#     username_validator = UnicodeUsernameValidator
#
#     username = models.CharField(
#         # _('username'),
#         max_length=150,
#         # help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
#         validators=[username_validator]
#     )
#     email = models.EmailField(
#         ('email address'),
#         unique=True
#     )
