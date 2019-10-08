from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'name', 'avatar', 'now_addr')

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if ret['avatar'] is not None:
            request = self.context.get('request')
            url = instance.avatar.url.url
            abs_url = request.build_absolute_uri(url)
            ret['avatar'] = abs_url
        return ret
