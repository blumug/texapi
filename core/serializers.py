from rest_framework import serializers


class ResultSerializer(serializers.Serializer):
    result = serializers.CharField(required=False)
