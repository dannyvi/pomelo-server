from rest_framework import serializers
from pomelo.buyer.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'name', 'avatar', 'now_addr')
        