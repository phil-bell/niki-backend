import json
import secrets
import uuid

from django.contrib.auth.models import User
from django.core.management.utils import get_random_secret_key
from django.db import models
from nacl.public import SealedBox


def generate_secret():
    return secrets.token_urlsafe(255)


class Server(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    owner = models.ForeignKey(
        User,
        related_name="owned_servers",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    public_key = models.CharField(max_length=255, blank=True, null=True)
    users = models.ManyToManyField(User, related_name="servers", blank=True)
    ip = models.GenericIPAddressField(blank=True, null=True)


class Location(models.Model):
    path = models.CharField(max_length=255, blank=True, null=True)
    server = models.ForeignKey(Server, on_delete=models.CASCADE, blank=True, null=True)


class Torrent(models.Model):
    magnet = models.CharField(max_length=255, blank=True, null=True)
    server = models.ForeignKey(Server, on_delete=models.CASCADE, blank=True, null=True)
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, blank=True, null=True
    )

    @property
    def data(self):
        return json.dumps(
            {"magnet": self.magnet, "location": self.location.path}
        ).encode("utf-8")

    def encrypt(self):
        box = SealedBox(self.server.public_key)
        return box.encrypt(self.data)
