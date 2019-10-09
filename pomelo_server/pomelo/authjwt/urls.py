from django.urls import path, include
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

from pomelo.settings import api_settings
from .views import BaseUserViewset, get_username

RouterClass = api_settings.DEFAULT_ROUTER
router = RouterClass()
router.register('user', BaseUserViewset)

app_name = 'authjwt'

token_response = openapi.Response(
    '',
    schema=openapi.Schema(
        _('Token'),
        type=openapi.TYPE_OBJECT,
        properties={
            'access': openapi.Schema(type=openapi.TYPE_STRING),
            'refresh': openapi.Schema(type=openapi.TYPE_STRING)
        })
)

refresh_response = openapi.Response(
    '',
    schema=openapi.Schema(
        _('Refresh'),
        type=openapi.TYPE_OBJECT,
        properties={
            'access': openapi.Schema(type=openapi.TYPE_STRING)
        })
)

token = method_decorator(name='post',
                         decorator=swagger_auto_schema(
                             operation_description=_('login for access token.'),
                             responses={'200':token_response})
                         )(TokenObtainPairView)
refresh = method_decorator(name='post',
                           decorator=swagger_auto_schema(
                               operation_description=_('refresh new access token.'),
                               responses={'200': refresh_response}
                           ))(TokenRefreshView)

urlpatterns = [
    path('token', token.as_view(), name='token_obtain_pair'),
    path('token/refresh', refresh.as_view(), name='token_refresh'),
    path('get_username', get_username, name='username'),
    path('', include((router.urls, 'buyer'), namespace='user')),
]
