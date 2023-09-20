from unittest.mock import call

import pytest
import pytest_asyncio
from channels.layers import get_channel_layer
from channels.routing import URLRouter
from channels.testing import WebsocketCommunicator
from django.contrib.auth.models import User
from django.urls import path, reverse

from api.consumers import ServerConsumer
from api.models import Location, Server


@pytest.fixture
def application():
    application = URLRouter(
        [
            path("server/<key>", ServerConsumer.as_asgi()),
        ]
    )
    yield application


@pytest.fixture
def server():
    user = User.objects.create(username="test", password="test")
    server = Server.objects.create(owner=user)
    location = Location.objects.create(path="test", server=server)
    yield server
    user.delete()
    server.delete()
    location.delete()


@pytest_asyncio.fixture
async def communicator(application, server):
    communicator = WebsocketCommunicator(
        application,
        f"/server/{server.key}",
        [(b"authentication", server.secret.encode())],
    )
    yield communicator
    await communicator.disconnect()


@pytest_asyncio.fixture
async def denied_communicator(application, server):
    communicator = WebsocketCommunicator(
        application,
        f"/server/{server.key}",
        [(b"authentication", b"incorrect_key")],
    )
    yield communicator
    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_server_consumer_connect(communicator):
    connected, _ = await communicator.connect()
    channel_layer = get_channel_layer()
    server = await Server.objects.afirst()

    assert connected
    assert len(channel_layer.groups) == 1
    assert server.key in channel_layer.groups


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_server_consumer_send_on_torrent_add_connect(
    mocker, async_client, communicator
):
    mock_send = mocker.patch("api.consumers.ServerConsumer.send_json")

    connected, _ = await communicator.connect()
    assert connected

    server = await Server.objects.afirst()
    location = await Location.objects.afirst()
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
    assert mock_send.mock_calls == [
        call(
            {
                "type": "torrent.add",
                "content": {
                    "magnet": "string",
                    "location": location.path,
                },
            }
        )
    ]


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_connection_refused_with_incorrect_secret(denied_communicator):
    connected, _ = await denied_communicator.connect()

    assert not connected
