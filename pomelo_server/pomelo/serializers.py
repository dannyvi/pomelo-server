from rest_framework import serializers


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
       style={'input_type': 'password'}
    )
