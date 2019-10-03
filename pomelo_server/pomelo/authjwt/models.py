from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _


# Create your models here.
class BaseUser(AbstractUser):
    phone = models.CharField(verbose_name=_('Phone Number'), null=True,
                             blank=True, default=None, unique=True,
                             max_length=20)
    email = models.EmailField(_('email address'), null=True, unique=True,
                              blank=True)
    REQUIRED_FIELDS = []

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
