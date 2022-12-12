from api.models import Location, Server, Torrent
from api.serializers import (LocationSerializer, ServerSerializer,
                             TorrentSerializer, UserSerializer)
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db.models import Q, QuerySet
from rest_framework import permissions, viewsets
from rest_framework_simplejwt.authentication import \
    JWTStatelessUserAuthentication


class AnonUserFilteredMixin:
    def get_queryset(self) -> QuerySet:
        if self.request.user.is_anonymous:
            return self.queryset.none()
        return self.queryset


class UserViewSet(viewsets.ModelViewSet, AnonUserFilteredMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer) -> User:
        serializer.validated_data["password"] = make_password(
            serializer.validated_data.pop("password")
        )
        return super().perform_create(serializer)


class ServerViewset(viewsets.ModelViewSet):
    queryset = Server.objects.all()
    serializer_class = ServerSerializer

    def get_queryset(self) -> QuerySet:
        return (
            super()
            .get_queryset()
            .filter(Q(owner=self.request.user) | Q(users__in=[self.request.user]))
        )


class LocationViewset(viewsets.ModelViewSet, AnonUserFilteredMixin):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    def get_queryset(self) -> QuerySet:
        return (
            super()
            .get_queryset()
            .filter(
                Q(server__owner=self.request.user)
                | Q(server__users__in=[self.request.user])
            )
        )


class TorrentViewset(viewsets.ModelViewSet, AnonUserFilteredMixin):
    queryset = Torrent.objects.all()
    serializer_class = TorrentSerializer

    def get_queryset(self) -> QuerySet:
        return (
            super()
            .get_queryset()
            .filter(
                Q(server__owner=self.request.user)
                | Q(server__users__in=[self.request.user])
            )
        )
