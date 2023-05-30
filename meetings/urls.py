from meetings.views import MeetingViewset
from rest_framework import renderers
from rest_framework.routers import format_suffix_patterns
from django.urls import path 

meeting_list = MeetingViewset.as_view({
    'get': 'list',
    'post': 'create'
})

meeting_detail = MeetingViewset.as_view({
    'get': 'retrieve',
    'put': 'update',
    'path': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path('meetings/', meeting_list, name='meetinglist'),
    path('meetings/<int:pk>/', meeting_detail, name="meetingdetail")
]
