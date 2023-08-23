from channels.generic.websocket import (
    AsyncJsonWebsocketConsumer,
    AsyncWebsocketConsumer,
)


class PocConsumer(AsyncWebsocketConsumer):
    groups = ["broadcast"]

    async def connect(self):
        await self.accept()
        await self.send(text_data="Hello there!")

    async def receive(self, text_data=None, bytes_data=None):
        await self.send(text_data="General Kanobi!")

    async def disconnect(self, close_code):
        pass


class ServerConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        key = self.scope["url_route"]["kwargs"]["key"]
        await self.channel_layer.group_add(key, self.channel_name)
        await self.accept()

    async def receive(self, content):
        await self.send_json({"content": content})

    async def torrent_add(self, event):
        await self.send_json({"type": "events.alarm", "content": event["content"]})

    async def disconnect(self, close_code):
        key = self.scope["url_route"]["kwargs"]["key"]
        self.channel_layer.group_discard(key, self.channel_name)
