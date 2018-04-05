import uuid

from django.db import models
from django.db.models import Q

from .Media import Media

from .maiofields import FixedCharField


#: Quick way of saying "NULL" for Django models
NULL = {'null': True, 'blank': True}


class Playlist(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    media = models.ManyToManyField(Media)
    name = models.CharField(max_length=1024)
    tn_path = models.CharField(max_length=1024)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    default_order = models.PositiveSmallIntegerField(default=0) # 0 random, 1 descending, 2 ascending
    seconds_between = models.FloatField(default=5.0)
    caption = models.TextField(**NULL)
    class Meta:
        ordering = ['-date_modified']
