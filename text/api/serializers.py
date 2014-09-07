from rest_framework import serializers

from text.models import Text


class AnalyzeSerializer(serializers.Serializer):

    url = serializers.CharField(required=True)


class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        exclude = ('user', )


class ResultSerializer(serializers.Serializer):

    success = serializers.BooleanField(required=True)
