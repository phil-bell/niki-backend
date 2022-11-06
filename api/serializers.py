from api.models import Location, Server, Torrent
from django.contrib.auth.models import User
from rest_framework import serializers


class UserValidatedMixin:
    def get_user_attribute(self, attr) -> User:
        return attr.get("user")

    def validate(self, attr):
        if self.context["request"].user != self.get_user_attribute(attr):
            raise serializers.ValidationError("User does not own this server")
        return super().validate(attr)


class UserSerializer(serializers.ModelSerializer, UserValidatedMixin):
    class Meta:
        model = User
        fields = ["pk", "url", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}


class ServerSerializer(serializers.ModelSerializer, UserValidatedMixin):
    class Meta:
        model = Server
        fields = [
            "pk",
            "url",
            "name",
            "secret",
        ]

    def create(self, validated_data) -> Server:
        server = super().create(validated_data)
        server.update(user=self.context["request"].user)
        return server


class LocationSerializer(serializers.ModelSerializer, UserValidatedMixin):
    class Meta:
        model = Location
        fields = [
            "pk",
            "url",
            "path",
            "server",
        ]

    def get_user_attribute(self, attr) -> User:
        return attr.get("server").user


class TorrentSerializer(serializers.ModelSerializer, UserValidatedMixin):
    class Meta:
        model = Torrent
        fields = [
            "pk",
            "url",
            "magnet",
            "server",
            "location",
        ]

    def get_user_attribute(self, attr) -> User:
        return attr.get("server").user
