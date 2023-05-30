from rest_framework.decorators import action 
from rest_framework.response import Response 
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework import renderers
from tutorials.models import (
    Tutorial,
    Student
)
from tutorials.serializers import (
    TutorialSerializer,
    StudentSerializer
)
# Create your views here.
class TutorialsViewset(viewsets.ModelViewSet):
    queryset = Tutorial.objects.all()
    serializer_class = TutorialSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(tuitor=self.request.user)

class JoinTutorial(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)