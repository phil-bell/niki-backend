from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db.models import Q, QuerySet
from django.http import Http404
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from the_python_bay import tpb

from api.models import Key, Location, Server, Torrent
from api.serializers import (
    KeySerializer,
    LocationSerializer,
    SearchSerializer,
    ServerSerializer,
    TorrentSerializer,
    UserSerializer,
)


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


class ServerViewset(
    viewsets.ModelViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
):
    queryset = Server.objects.all()
    serializer_class = ServerSerializer

    def get_queryset(self) -> QuerySet:
        try:
            return (
                super()
                .get_queryset()
                .filter(Q(owner=self.request.user) | Q(users__in=[self.request.user]))
            )
        except TypeError:
            raise Http404


class LocationViewset(
    viewsets.ModelViewSet,
    AnonUserFilteredMixin,
    mixins.ListModelMixin,
):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    def get_queryset(self) -> QuerySet:
        try:
            return (
                super()
                .get_queryset()
                .filter(
                    Q(server__owner=self.request.user)
                    | Q(server__users__in=[self.request.user.id])
                )
            )
        except TypeError:
            raise Http404


class TorrentViewset(viewsets.ModelViewSet, AnonUserFilteredMixin):
    queryset = Torrent.objects.all()
    serializer_class = TorrentSerializer

    def get_queryset(self) -> QuerySet:
        try:
            return (
                super()
                .get_queryset()
                .filter(
                    Q(server__owner=self.request.user)
                    | Q(server__users__in=[self.request.user.id])
                )
            )
        except TypeError:
            raise Http404


class KeyViewset(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Key.objects.all()
    serializer_class = KeySerializer


class SearchView(APIView):
    def post(self, request, format=None):
        serializer = SearchSerializer(data=request.data)
        if serializer.is_valid():
            results = tpb.search(serializer.validated_data["term"])
            return Response(
                [result.to_dict for result in results], status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
