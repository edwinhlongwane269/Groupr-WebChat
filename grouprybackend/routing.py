from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import g_auth.routing
import groups.routing

application = ProtocolTypeRouter({
    # This is where you can define routes for different protocols using URLRouter
    # for django authentication to work we wrap it 
    # with a AuthMiddlewarestack
    'websocket': AuthMiddlewareStack(
        URLRouter(g_auth.routing.websocket_routes),
        URLRouter(groups.routing.websocket_urlpatterns)
    ),
})