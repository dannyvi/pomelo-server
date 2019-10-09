from django.db import models
from pomelo.settings import api_settings
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from django.db.models.signals import post_save
from django.dispatch import receiver

UserModel = get_user_model()


class Address(models.Model):
    """收货地址。"""
    name = models.CharField(verbose_name=_('Receiver'), null=True, blank=True, default=None, max_length=50)
    mobile = models.CharField(verbose_name=_('Mobile'), null=True, blank=True, default=None, max_length=20)
    area = models.CharField(verbose_name=_('Area'), null=True, blank=True, default=None, max_length=30)
    text = models.TextField(_('Address'))
    owner = models.ForeignKey(api_settings.PROFILE_MODEL, verbose_name=_('Owner'), related_name='addresses',
                              blank=True, null=True, default=None, on_delete=models.DO_NOTHING)


class Buyer(UserModel):
    """Inherit UserModel from settings.AUTH_USER_MODEL"""

    class Meta:
        proxy = True


class Profile(models.Model):
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(verbose_name=_('Name'), null=True, blank=True, default=None, max_length=40)
    avatar = models.OneToOneField(api_settings.IMAGE_MODEL, verbose_name=_('Avatar'), null=True, blank=True,
                                  default=None, on_delete=models.DO_NOTHING)
    now_addr = models.OneToOneField(Address, verbose_name=_('Current Address'), blank=True, null=True, default=None,
                                    on_delete=models.DO_NOTHING)


@receiver(post_save, sender=UserModel)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(owner=instance)


@receiver(post_save, sender=UserModel)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
