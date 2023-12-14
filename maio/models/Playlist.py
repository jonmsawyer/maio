'''
File: Playlist.py

Module: ``maio.models.Playlist``
'''

from __future__ import annotations

import uuid

from django.db.models import (
    Model, UUIDField, ManyToManyField, CharField, DateTimeField, PositiveSmallIntegerField,
    FloatField, TextField, ForeignKey, DO_NOTHING,
)
from django.db.models.base import ModelBase

from .Media import Media
from .MaioMapType import MaioMapType


class PlaylistMeta(ModelBase):
    '''Metaclass for Playlist model.'''
    ordering = ['-date_modified']


class Playlist(Model, metaclass=PlaylistMeta):
    '''Playlist model.'''
    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    media: ManyToManyField[Media, Playlist] = ManyToManyField(Media)
    name = CharField(max_length=1024)
    tn_path = CharField(max_length=1024)
    date_added = DateTimeField(auto_now_add=True)
    date_modified = DateTimeField(auto_now=True)
    default_order = PositiveSmallIntegerField(default=0) # 0 random, 1 descending, 2 ascending
    seconds_between = FloatField(default=5.0)
    caption_type = ForeignKey(to=MaioMapType, on_delete=DO_NOTHING, default=MaioMapType.default)
    caption = TextField(null=True, blank=True)
