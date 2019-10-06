from django.urls import path, include
#from pomelo.settings import api_settings
from rest_framework.routers import DefaultRouter
from .views import ProfileViewset

#RouterClass = api_settings.DEFAULT_ROUTER
router = DefaultRouter(trailing_slash=False)
router.register('profile', ProfileViewset)

urlpatterns = [
    path('', include((router.urls, 'buyer_manage'), namespace='buyer')),
]
