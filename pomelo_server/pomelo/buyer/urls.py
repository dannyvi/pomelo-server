from django.urls import path, include
from pomelo.settings import api_settings
# from rest_framework.routers import DefaultRouter
from .views import ProfileViewSet

# RouterClass = api_settings.DEFAULT_ROUTER
# router = DefaultRouter(trailing_slash=False)

RouterClass = api_settings.DEFAULT_ROUTER
router = RouterClass()
router.register('profile', ProfileViewSet)

urlpatterns = [
    path('', include((router.urls, 'buyer_manage'), namespace='buyer')),
]
