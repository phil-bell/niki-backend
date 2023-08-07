import pytest
from channels.routing import URLRouter
from channels.testing import WebsocketCommunicator
from django.urls import path

from api.consumers import PocConsumer, ServerConsumer
from api.models import Server


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_poc_consumer_connect():
    communicator = WebsocketCommunicator(PocConsumer.as_asgi(), "/server/")
    connected, _ = await communicator.connect()
    assert connected
    # Test on connection welcome message
    message = await communicator.receive_from()
    assert message == "Hello there!"

    await communicator.send_to(text_data="test")
    message = await communicator.receive_from()
    assert message == "General Kanobi!"

    # Close
    await communicator.disconnect()


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_server_consumer_connect():
    server = Server.objects.create()
    application = URLRouter(
        [
            path("server/<key>", ServerConsumer.as_asgi()),
        ]
    )
    communicator = WebsocketCommunicator(application, f"/server/{server.key}")
    connected, _ = await communicator.connect()
    assert connected
    # Test on connection welcome message
    message = await communicator.receive_json_from()
    assert message == {"status": "connected", "key": server.key}
    assert communicator.scope["kwargs"] == "testing"

    await communicator.disconnect()
