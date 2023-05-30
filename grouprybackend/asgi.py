import os

from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import g_auth.routing
from groups.consumers import GroupConsumer
from django.conf import settings 
from django_nextjs.proxy import NextJSProxyHttpConsumer, NextJSProxyWebsocketConsumer
from django.urls import re_path, path
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grouprybackend.settings')
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()
websocket_routers = [
    re_path(r'ws/groups/%', GroupConsumer.as_asgi()),
]


application = ProtocolTypeRouter({
    # This is where you can define routes for different protocols using URLRouter
    # for django authentication to work we wrap it 
    # with a AuthMiddlewarestack
    "http": django_asgi_app,
    'websocket': AuthMiddlewareStack(
        URLRouter(websocket_routers),
    ),
})
