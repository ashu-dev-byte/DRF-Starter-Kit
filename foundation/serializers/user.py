from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ["id", "email", "is_active", "age", "role", "created_at", "updated_at"]


class UserWithTokenSerializer(UserSerializer):
    access_token = serializers.CharField()

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ["access_token"]
