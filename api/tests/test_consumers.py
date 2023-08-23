import pytest
from asgiref.sync import sync_to_async
from channels.routing import URLRouter
from channels.testing import WebsocketCommunicator
from django.contrib.auth.models import User
from django.urls import path, reverse

from api.consumers import PocConsumer, ServerConsumer
from api.models import Location, Server


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_poc_consumer_connect():
    communicator = WebsocketCommunicator(PocConsumer.as_asgi(), "/server/")
    connected, _ = await communicator.connect()
    assert connected

    message = await communicator.receive_from()
    assert message == "Hello there!"

    await communicator.send_to(text_data="test")
    message = await communicator.receive_from()
    assert message == "General Kanobi!"

    # Close
    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_server_consumer_connect(mocker):
    server = await Server.objects.acreate()
    application = URLRouter(
        [
            path("server/<key>", ServerConsumer.as_asgi()),
        ]
    )

    communicator = WebsocketCommunicator(application, f"/server/{server.key}")
    connected, _ = await communicator.connect()
    assert connected

    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_server_consumer_send_on_torrent_add_connect(
    mocker,
    async_client,
):
    mock_send = mocker.patch("api.consumers.ServerConsumer.send")

    user = await User.objects.acreate(username="test", password="test")
    server = await Server.objects.acreate(owner=user)
    location = await Location.objects.acreate(path="test", server=server)

    application = URLRouter(
        [
            path("server/<key>", ServerConsumer.as_asgi()),
        ]
    )

    communicator = WebsocketCommunicator(application, f"/server/{server.key}")
    connected, _ = await communicator.connect()
    assert connected

    url = reverse("torrent-list")
    response = await async_client.post(
        url,
        data={
            "magnet": "string",
            "server": server.pk,
            "location": location.pk,
        },
    )

    assert response.status_code == 201
    assert mock_send.mock_calls == []

    await communicator.disconnect()
