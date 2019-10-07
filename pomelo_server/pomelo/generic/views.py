from rest_framework.viewsets import ModelViewSet
from .models import Image
from .serializers import ImageSerializer
from rest_framework import permissions


class ImageViewSet(ModelViewSet):
    """Image Management Viewset."""
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
