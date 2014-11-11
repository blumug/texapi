from rest_framework import serializers

from text.models import Text


class AnalyzeSerializer(serializers.Serializer):

    url = serializers.CharField(required=True)


class TextSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField('get_id')

    def get_id(self, obj):
        return obj.task_id

    class Meta:
        model = Text
        exclude = ('user', 'task_id')


class ResultSerializer(serializers.Serializer):

    success = serializers.BooleanField(required=True)
