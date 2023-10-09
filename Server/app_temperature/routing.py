from django.urls import path
from . import consumers

websocket_urlspatterns = [
    path('ws/temperature/',consumers.TemperatureConsumer.as_asgi(),)
]
