from django.db import models
from pomelo.settings import api_settings
from django.conf import settings
from django.utils.translation import gettext as _, gettext_lazy


class Address(models.Model):
    """收货地址。"""
    name = models.CharField(verbose_name=_('Receiver'), null=True, blank=True, default=None, max_length=50)
    mobile = models.CharField(verbose_name=_('Mobile'), null=True, blank=True, default=None, max_length=20)
    area = models.CharField(verbose_name=_('Area'), null=True, blank=True, default=None, max_length=30)
    text = models.TextField(_('Address'))
    owner = models.ForeignKey(api_settings.BUYER_MODEL, verbose_name=_('Owner'), related_name='addresses', blank=True, null=True, default=None, on_delete=models.DO_NOTHING)


class Profile(models.Model):
    name = models.CharField(verbose_name=_('Name'), null=True, blank=True, default=None, max_length=40)
    avatar = models.OneToOneField('pomelo.Picture', verbose_name=_('Avatar'), null=True, blank=True, default=None, on_delete=models.DO_NOTHING)
    now_addr = models.OneToOneField(Address, verbose_name=_('Current Address'), blank=True, null=True, default=None, on_delete=models.DO_NOTHING)


class Buyer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name=_('User'), on_delete=models.CASCADE)
    profile = models.OneToOneField(Profile, verbose_name=_('Profile'), on_delete=models.CASCADE)

 