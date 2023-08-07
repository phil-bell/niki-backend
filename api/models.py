import json
import secrets

from django.contrib.auth.models import User
from django.db import models
from nacl.encoding import HexEncoder
from nacl.public import PrivateKey, PublicKey, SealedBox


def generate_key():
    return secrets.token_urlsafe(64)


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
    key = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        default=generate_key,
    )
    secret = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        default=generate_secret,
    )

    users = models.ManyToManyField(User, related_name="servers", blank=True)
    address = models.CharField(max_length=255, blank=True, null=True)


class Location(models.Model):
    path = models.CharField(max_length=255, blank=True, null=True)
    server = models.ForeignKey(
        Server,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )


class Torrent(models.Model):
    magnet = models.TextField(blank=True, null=True)
    server = models.ForeignKey(
        Server,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, blank=True, null=True
    )

    @property
    def data(self):
        return json.dumps(
            {"magnet": self.magnet, "location": self.location.path}
        ).encode()

    def encrypt(self):
        box = SealedBox(
            PublicKey(self.server.public_key.encode(), encoder=HexEncoder),
        )
        return box.encrypt(self.data)


class Key(models.Model):
    private_key = models.CharField(max_length=64, blank=True, null=True)
    public_key = models.CharField(max_length=64, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            private_key = PrivateKey.generate()
            self.private_key = private_key.encode(encoder=HexEncoder).decode()
            self.public_key = private_key.public_key.encode(encoder=HexEncoder).decode()
        super(Key, self).save(*args, **kwargs)
