from api.models import Location, Server, Torrent
from api.serializers import (LocationSerializer, ServerSerializer,
                             TorrentSerializer, UserSerializer)
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db.models import QuerySet
from rest_framework import permissions, viewsets
from rest_framework_simplejwt.authentication import \
    JWTStatelessUserAuthentication


class UserFilteredMixin:
    user_pk_relation = "pk"

    def get_queryset(self) -> QuerySet:
        if self.request.user.is_anonymous:
            return self.queryset.none()
        elif self.request.user.is_superuser:
            return self.queryset
        return self.queryset.filter(**{self.user_pk_relation: self.request.user.pk})


class UserViewSet(viewsets.ModelViewSet, UserFilteredMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer) -> User:
        serializer.validated_data["password"] = make_password(
            serializer.validated_data.pop("password")
        )
        return super().perform_create(serializer)


class ServerViewset(viewsets.ModelViewSet, UserFilteredMixin):
    queryset = Server.objects.all()
    serializer_class = ServerSerializer
    user_pk_relation = "user__pk"


class LocationViewset(viewsets.ModelViewSet, UserFilteredMixin):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    user_pk_relation = "server__user__pk"


class TorrentViewset(viewsets.ModelViewSet, UserFilteredMixin):
    queryset = Torrent.objects.all()
    serializer_class = TorrentSerializer
    user_pk_relation = "server__user__pk"
