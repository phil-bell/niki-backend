import uuid

from django.contrib.auth.models import Group, Permission, User
from django.db import models

# Create your models here.


class Server(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    secret = models.UUIDField(default=uuid.uuid4, editable=False)


class Location(models.Model):
    path = models.CharField(max_length=255)
    server = models.ForeignKey(Server, on_delete=models.CASCADE)


class Torrent(models.Model):
    magnet = models.CharField(max_length=255)
    server = models.ForeignKey(Server, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
