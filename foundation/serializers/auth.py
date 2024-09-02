from rest_framework import serializers


class RegisterUserSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=3, max_length=256)
    email = serializers.EmailField(max_length=256)
    password = serializers.CharField(min_length=8, write_only=True)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
