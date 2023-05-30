from rest_framework.decorators import action 
from rest_framework.response import Response 
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework import renderers
from meetings.serializers import MeetingSerializer
from meetings.models import Meeting

# Create your views here.
class MeetingViewset(viewsets.ModelViewSet):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        return super().perform_create(serializer)