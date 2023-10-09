import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import app_temperature.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Server.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': URLRouter(
        app_temperature.routing.websocket_urlspatterns
    )
})
