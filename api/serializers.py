from api.models import Location, Server, Torrent
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["pk", "url", "username", "password"]


class ServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Server
        fields = [
            "pk",
            "url",
            "name",
            "user",
            "secret",
        ]


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
