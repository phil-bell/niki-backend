import uuid

from django.contrib.auth.models import User
from django.core.management.utils import get_random_secret_key
from django.db import models


def generate_secret():
    return secrets.token_urlsafe(255)


class Server(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(
        User,
        related_name="owned_servers",
        on_delete=models.CASCADE,
    )
    key = models.UUIDField(default=uuid.uuid4)
    secret = models.CharField(default=generate_secret, max_length=255)
    users = models.ManyToManyField(User, related_name="servers")


class Location(models.Model):
    path = models.CharField(max_length=255)
    server = models.ForeignKey(Server, on_delete=models.CASCADE)


class Torrent(models.Model):
    magnet = models.CharField(max_length=255)
    server = models.ForeignKey(Server, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
