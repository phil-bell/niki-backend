import logging

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.models import User
from rest_framework import serializers

from api.models import Key, Location, Server, Torrent

_logger = logging.getLogger(__package__)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "pk",
            "url",
            "username",
            "password",
        ]
        extra_kwargs = {"password": {"write_only": True}}


class ServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Server
        fields = [
            "pk",
            "url",
            "name",
            "owner",
            "public_key",
            "users",
            "address",
        ]

    def create(self, *args, **kwargs):
        instance = super().create(*args, **kwargs)
        instance.owner = self.context["request"].user
        instance.save()
        return instance


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = [
            "pk",
            "url",
            "path",
            "server",
        ]


class TorrentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Torrent
        fields = [
            "pk",
            "url",
            "magnet",
            "server",
            "location",
        ]

    def create(self, *args, **kwargs):
        instance = super().create(*args, **kwargs)
        channel_layer = get_channel_layer()
        print(channel_layer)
        async_to_sync(channel_layer.group_send)(
            instance.server.key,
            {
                "type": "torrent.add",
                "content": {
                    "magnet": instance.magnet,
                    "location": instance.location.path,
                },
            },
        )
        return instance


class KeySerializer(serializers.ModelSerializer):
    class Meta:
        model = Key
        fields = ["public_key"]


class SearchSerializer(serializers.Serializer):
    term = serializers.CharField()

    class Meta:
        fields = ["term"]
