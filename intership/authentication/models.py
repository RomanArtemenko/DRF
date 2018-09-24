from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import AbstractUser, UserManager
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# Create your models here.


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class MyUserManager(UserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
         Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            ** extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)


class MyUser(AbstractUser):
    username_validator = UnicodeUsernameValidator

    username = models.CharField(
        verbose_name='username',
        max_length=150,
        validators=[username_validator]
    )
    email = models.EmailField(
        verbose_name='email address',
        unique=True
    )

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return self.email


# class UserProfile(models.Model):
#     user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
#     phone_number = models.CharField(max_length=12, blank=False)
#     social_id = models.CharField(max_length= 128, blank=True)
#     nickname = models.CharField(max_length=50, default='')
