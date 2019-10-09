from rest_framework.viewsets import ModelViewSet
from .models import Image
from .serializers import ImageSerializer
from rest_framework import permissions
from django.utils.translation import gettext_lazy as _
from drf_yasg.utils import swagger_auto_schema as sas
from drf_yasg import openapi
from django.utils.decorators import method_decorator as md
from rest_framework import serializers
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser


class ImageUploadSerializer(serializers.Serializer):
    url = serializers.ImageField(help_text=_("Upload image."))


@md(name='create', decorator=sas(manual_parameters=[openapi.Parameter('url', openapi.IN_FORM, description=_('Upload image.'), type=openapi.TYPE_FILE), ]))
@parser_classes([MultiPartParser, ])
class ImageViewSet(ModelViewSet):
    """Image Management Viewset."""
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

