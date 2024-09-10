from rest_framework import serializers


class ValidationErrSerializer(serializers.Serializer):
    errors = serializers.DictField(child=serializers.CharField())


class ErrRespSerializer(serializers.Serializer):
    message = serializers.CharField()
