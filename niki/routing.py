from django.urls import path

from api.consumers import ServerConsumer

websocket_urlpatterns = [
    path("server/<key>", ServerConsumer().as_asgi()),
]
