from django.urls import path, include
from pomelo.settings import pomelo_settings
from .views import ImageViewSet


RouterClass = pomelo_settings.DEFAULT_ROUTER
router = RouterClass()
router.register('image', ImageViewSet)

urlpatterns = [
    path('', include((router.urls, 'pomelo'), namespace='pomelo')),
]
