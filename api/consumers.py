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
        # Called when the socket closes
        pass


class ServerConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send_json(
            {
                "status": "connected",
                "key": self.scope["url_route"]["kwargs"]["key"],
            }
        )

    async def receive(self, content):
        await self.send_json({"content": content})

    async def disconnect(self, close_code):
        # Called when the socket closes
        pass
