from api.models import Location, Server, Torrent
from api.serializers import (LocationSerializer, ServerSerializer,
                             TorrentSerializer, UserSerializer)
from django.contrib.auth.models import User
from rest_framework import viewsets


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ServerViewset(viewsets.ModelViewSet):
    queryset = Server.objects.all()
    serializer = ServerSerializer

    def get_queryset(self):
        self.queryset.filter(user=self.user)


class LocationViewset(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer = LocationSerializer

    def get_queryset(self):
        self.queryset.filter(server__user=self.user)


class TorrentViewset(viewsets.ModelViewSet):
    queryset = Torrent.objects.all()
    serializer = TorrentSerializer

    def get_queryset(self):
        self.queryset.filter(server__user=self.user)
