from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

from pomelo.settings import api_settings
from .views import BaseUserViewset, get_username

RouterClass = api_settings.DEFAULT_ROUTER
router = RouterClass(trailing_slash=False)
router.register('user', BaseUserViewset)

urlpatterns = [
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('get_username', get_username),
    path('', include((router.urls, 'user_manage'), namespace='user')),
]
