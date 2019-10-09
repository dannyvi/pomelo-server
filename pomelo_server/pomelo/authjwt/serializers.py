from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist

from pomelo.errors import FieldError

import random
import string

User = get_user_model()


def get_random_string(slen=40):
    return ''.join(random.sample(string.ascii_letters + string.digits, slen))


def get_valid_username():
    username = get_random_string()
    try:
        User.objects.get(username=username)
        return get_valid_username()
    except ObjectDoesNotExist:
        return username


class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'phone', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True},
                        'username': {'required': False}}

    def create(self, validated_data):
        """create BaseUser instance."""
        email = validated_data.pop("email", None)
        phone = validated_data.pop("phone", None)
        if email is None and phone is None:
            raise FieldError(_("email or phone field required"))
        username = get_valid_username()
        validated_data.update(username=username, email=email, phone=phone)
        password = validated_data.pop('password', None)
        user = self.Meta.model(**validated_data)
        # user.is_staff = True
        if password is not None:
            user.set_password(password)
        user.save()
        return user


class UserNameSerializer(serializers.ModelSerializer):
    """query username"""
    class Meta:
        model = User
        fields = ('username', )
        read_only_fields = ('username', )
