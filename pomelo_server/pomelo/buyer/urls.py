from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfileViewset

router = DefaultRouter(trailing_slash=False)
router.register('profile', ProfileViewset)

urlpatterns = [
    path('', include((router.urls, 'buyer_manage'), namespace='buyer')),
]
