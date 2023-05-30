from rest_framework import renderers
from rest_framework.routers import format_suffix_patterns
from django.urls import path
from tutorials.views import (
    TutorialsViewset,   
)

tutorial_list = TutorialsViewset.as_view({
    'get': 'list',
    'post': 'create'
})

tutorial_detail = TutorialsViewset.as_view({
    'get': 'retrieve',
    'put': 'update',
    'path': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path('tutorials', tutorial_list, name="tutorials"),
    path('tutorials/<int:pk>/', tutorial_detail, name="tutorialdetail")
]
