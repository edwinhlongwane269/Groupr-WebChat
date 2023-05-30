from g_auth.models import G_AUTH_USER_MODEL
from .serializers import GUserSerializer
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    PatchModelMixin,
    UpdateModelMixin,
    CreateModelMixin,
    DeleteModelMixin,
)


class GUserConsumer( ListModelMixin, RetrieveModelMixin, PatchModelMixin, UpdateModelMixin, CreateModelMixin, DeleteModelMixin,GenericAsyncAPIConsumer):
    queryset = G_AUTH_USER_MODEL.objects.all()
    serializer_class = GUserSerializer

    
