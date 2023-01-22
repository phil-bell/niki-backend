import requests
from api.models import Location, Server, Torrent
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["pk", "url", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}


class ServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Server
        fields = [
            "pk",
            "url",
            "key",
            "name",
            "public_key",
            "users",
            "owner",
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
        response = requests.post(instance.server.ip, data=instance.encrypt())
        return instance
