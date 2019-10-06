from django.db import models
from django.utils.translation import gettext as _


class Picture(models.Model):
    title = models.CharField(verbose_name=_('Name'), null=True, blank=True, default=None, max_length=40)
    linkage = models.URLField(verbose_name=_('Web Address'), null=True, blank=True, default=None, max_length=256)
