from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import apps.chat.routing
from apps.chat import routing

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            #apps.chat.routing.websocket_urlpatterns
            routing.websocket_urlpatterns
        )
    ),
})
