from api.models import Location, Server, Torrent
from api.serializers import (LocationSerializer, ServerSerializer,
                             TorrentSerializer, UserSerializer)
from django.contrib.auth.models import User
from rest_framework import viewsets


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_questset(self):
        self.queryset.filter(pk=self.request.user.pk)


class ServerViewset(viewsets.ModelViewSet):
    queryset = Server.objects.all()
    serializer_class = ServerSerializer

    def get_queryset(self):
        self.queryset.filter(user=self.request.user)


class LocationViewset(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    def get_queryset(self):
        self.queryset.filter(server__user=self.request.user)


class TorrentViewset(viewsets.ModelViewSet):
    queryset = Torrent.objects.all()
    serializer_class = TorrentSerializer

    def get_queryset(self):
        self.queryset.filter(server__user=self.request.user)
