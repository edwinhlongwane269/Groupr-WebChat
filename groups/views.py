from rest_framework.decorators import action 
from rest_framework.response import Response 
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework import renderers
from groups.models import Group
from groups.serializers import GroupSerializer
from rest_framework.decorators import api_view

# Create your views here.
class GroupViewset(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrive`,
    additionally also provides an extra `highlight` action
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    @action(detail=True, renderer_class=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        group = self.get_object()
        return Response(group.highlight)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

@api_view(['POST'])
def join_group():
    pass