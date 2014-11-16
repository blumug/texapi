from rest_framework.response import Response
from rest_framework import generics
from rest_framework import permissions

from serializers import ResultSerializer, AnalyzeSerializer, TextSerializer
from text.models import Text
from text import tasks
from core.exceptions import BadArgumentErrorException


class TextPermission(permissions.BasePermission):
    """Permission for text
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated() is False:
            return False
        else:
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated() is False:
            return False
        return obj.user.id == request.user.id


class AnalyzeView(generics.CreateAPIView):
    """
    Analyze text
    """
    serializer_class = AnalyzeSerializer
    permission_classes = (TextPermission, )

    def is_banned(self, url):
        """
        Check for special urls (localhost, 127.0.0.1, ...)

        Returns:
            true if url is forbidden
        """
        if url is None:
            return True
        if url.startswith('http://localhost'):
            return True
        if url.startswith('https://localhost'):
            return True
        if url.startswith('http://127.0.0.1'):
            return True
        if url.startswith('https://127.0.0.1'):
            return True
        return False

    def post(self, request, *args, **kwargs):
        """
        Start a new analysis
        """
        serializer = self.serializer_class(data=request.DATA)
        if serializer.is_valid():
            url = serializer.object['url']
            if self.is_banned(url):
                raise BadArgumentErrorException()
            text, _created = Text.objects.get_or_create(url=url, user=request.user)
            result = tasks.process_text.delay(text.id)
            Text.objects.filter(id=text.id).update(task_id=result.id)
            text.task_id = result.id
            self.serializer_class = TextSerializer
            serializer = self.get_serializer(text)
            return Response(serializer.data)

        else:
            self.serializer_class = ResultSerializer
            serializer = self.get_serializer({'success': False})
            return Response(serializer.data)
analyze = AnalyzeView.as_view()


class TextsView(generics.ListAPIView):
    """
    List texts
    """
    permission_classes = (TextPermission, )
    serializer_class = TextSerializer
    model = Text
texts = TextsView.as_view()


class TextView(generics.RetrieveAPIView):
    """
    Retrieve text
    """
    permission_classes = (TextPermission, )
    serializer_class = TextSerializer
    model = Text
    lookup_field = 'task_id'
text = TextView.as_view()
