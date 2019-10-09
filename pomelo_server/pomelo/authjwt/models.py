from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class BaseUser(AbstractUser):
    phone = models.CharField(verbose_name=_('Phone'), null=True, blank=True, default=None,
                             unique=True, max_length=20)
    email = models.EmailField(_('email address'), null=True, unique=True, blank=True)
    REQUIRED_FIELDS = ['email']

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
