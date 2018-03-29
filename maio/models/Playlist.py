import uuid

from django.db import models
from django.db.models import Q

from .maiofields import FixedCharField


class Playlist(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=1024)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)
    default_order = models.PositiveSmallIntegerField(default=0) # 0 random, 1 descending, 2 ascending
    seconds_between = models.FloatField(default=5.0)
    media_class = models.PositiveSmallIntegerField(default=0) # 0 other, 1 image, 2 video, 3 audio, 4 document
    caption = models.TextField(null=True, blank=True)
    class Meta:
        ordering = ['-date_modified']
