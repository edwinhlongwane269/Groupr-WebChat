from django.urls import re_path
from groups import consumers

websocket_urlpatterns = [
    re_path(r'ws/groupchats/group/$', consumers.GroupConsumer.as_asgi()),
]