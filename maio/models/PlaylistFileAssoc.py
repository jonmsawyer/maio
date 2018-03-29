import uuid

from django.db import models
from django.db.models import Q

from .File import File
from .Playlist import Playlist
from .maiofields import FixedCharField


class PlaylistFileAssoc(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    sort = models.PositiveIntegerField()
    
    
    class Meta:
        ordering = ['playlist']
