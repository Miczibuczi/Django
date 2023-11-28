from django.urls import path, include
from chat.consumers import ChatConsumer

websocket_urlpattenrs = [
    path("", ChatConsumer.as_asgi()),
]