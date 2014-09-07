from rest_framework import serializers


class AnalyzeSerializer(serializers.Serializer):

    url = serializers.CharField(required=True)


class ResultSerializer(serializers.Serializer):

    success = serializers.BooleanField(required=True)
