from rest_framework.viewsets import ModelViewSet
from pomelo.buyer.models import Profile
from pomelo.buyer.serializers import ProfileSerializer
from rest_framework import permissions


class ProfileViewset(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.AllowAny]
