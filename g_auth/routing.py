from django.urls import re_path
from g_auth.consumers import GUserConsumer

websocket_urlpatterns = [
    re_path(r"^ws/users/$", GUserConsumer.as_asgi()),
]