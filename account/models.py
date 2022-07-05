import uuid

from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile", unique=True
    )
    secret_key = models.UUIDField(default=uuid.uuid4().hex)
    server_address = models.CharField(
        max_length=255, unique=True, null=True, blank=True
    )
