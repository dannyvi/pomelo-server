from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from rest_framework.routers import DefaultRouter
from pomelo.authjwt.views import get_username
from .views import BaseUserViewset

router = DefaultRouter(trailing_slash=False)
router.register('buyer', BaseUserViewset)

urlpatterns = [
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('get_username', get_username),
    path('', include((router.urls, 'buyer_manage'), namespace='buyer')),
]
