from groups.views import GroupViewset
from rest_framework import renderers
from rest_framework.routers import format_suffix_patterns
from django.urls import path

group_list = GroupViewset.as_view({
    'get': 'list',
    'post': 'create'
})

group_detail = GroupViewset.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

group_highlight = GroupViewset.as_view({
    'get': 'highlight'
}, renderer_classes=[renderers.StaticHTMLRenderer])

urlpatterns = [
    path('groups/', group_list, name="grouplist"),
    path('groups/<int:pk>/', group_detail, name="group-detail"),
    path('groups/<int:pk>/highlight/', group_highlight, name="group-highlight"),
]
