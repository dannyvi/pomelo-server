from django.conf import settings
from django.test.signals import setting_changed
from django.utils.translation import gettext_lazy as _
from rest_framework.settings import APISettings as _APISettings

from .utils import format_lazy

USER_SETTINGS = getattr(settings, 'POMELO', None)

DEFAULTS = {
    'SIGNING_KEY': settings.SECRET_KEY,
    'VERIFYING_KEY': None,
    'PROFILE_MODEL': 'buyer.Profile',
    'IMAGE_MODEL': 'generic.Image',

    'DEFAULT_ROUTER': 'pomelo.routers.MinorRouter'
}

IMPORT_STRINGS = (
    'DEFAULT_ROUTER',
)

REMOVED_SETTINGS = (
)


class APISettings(_APISettings):  # pragma: no cover
    def __check_user_settings(self, user_settings):
        SETTINGS_DOC = 'https://github.com/dannyvi/pomelo/settings'

        for setting in REMOVED_SETTINGS:
            if setting in user_settings:
                raise RuntimeError(format_lazy(
                    _("The '{}' setting has been removed. Please refer to '{}' for available settings."),
                    setting, SETTINGS_DOC,
                ))

        return user_settings


api_settings = APISettings(USER_SETTINGS, DEFAULTS, IMPORT_STRINGS)


def reload_api_settings(*args, **kwargs):  # pragma: no cover
    global api_settings

    setting, value = kwargs['setting'], kwargs['value']

    if setting == 'POMELO':
        api_settings = APISettings(value, DEFAULTS, IMPORT_STRINGS)


setting_changed.connect(reload_api_settings)
