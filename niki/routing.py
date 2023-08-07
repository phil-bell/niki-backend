from django.urls import path

from api.consumers import PocConsumer

websocket_urlpatterns = [
    path("server/", PocConsumer.as_asgi()),
]
