from rest_framework.response import Response
from rest_framework import generics
from rest_framework import permissions

from serializers import ResultSerializer, AnalyzeSerializer


class TextPermission(permissions.BasePermission):
    """Permission for text:
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated() is False:
            return False
        else:
            return True

    def has_object_permission(self, request, view, obj):
        return True


class AnalyzeView(generics.CreateAPIView):
    """
    Analyze text
    """
    serializer_class = AnalyzeSerializer
    permission_classes = (TextPermission, )

    def post(self, request, *args, **kwargs):
        """
        Create a new attachement
        """
        serializer = self.serializer_class(data=request.DATA)
        if serializer.is_valid():
            url = serializer.object['url']

        self.serializer_class = ResultSerializer()
        serializer = self.get_serializer({'success': True})
        return Response(serializer.data)
analyze = AnalyzeView.as_view()
