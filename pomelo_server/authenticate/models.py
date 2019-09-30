from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class BaseUser(AbstractUser):
    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
