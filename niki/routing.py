from django.urls import path

from api.consumers import PocConsumer, ServerConsumer

websocket_urlpatterns = [
    path("", PocConsumer.as_asgi()),
    path("server/<key>", ServerConsumer().as_asgi()),
]
