from channels.exceptions import DenyConnection
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from api.models import Server


class ServerConsumer(AsyncJsonWebsocketConsumer):
    @property
    def headers(self):
        return {key.decode(): value.decode() for key, value in self.scope["headers"]}

    @property
    def key(self):
        return self.scope["url_route"]["kwargs"]["key"]

    async def authenticate(self):
        self.server = await Server.objects.filter(
            key=self.key, secret=self.headers.get("authentication")
        ).afirst()
        print(f"{self.key=}")
        print(f"{self.headers.get('authentication')=}")
        print(f"{self.server}")
        if not self.server:
            raise DenyConnection
        await self.accept()

    async def connect(self):
        await self.authenticate()
        await self.channel_layer.group_add(self.key, self.channel_name)

    async def receive(self, content):
        await self.send_json({"content": content})

    async def torrent_add(self, event):
        await self.send_json({"type": "torrent.add", "content": event["content"]})

    async def disconnect(self, close_code):
        self.channel_layer.group_discard(self.key, self.channel_name)
        self.server = None
