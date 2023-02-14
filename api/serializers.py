import requests
from django.contrib.auth.models import User
from rest_framework import serializers

from api.models import Location, Server, Torrent


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
        data = instance.encrypt()
        response = requests.post(
            f"{instance.server.address}/add/",
            data=data,
        )
        
        return instance
