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
    class Meta:
        verbose_name = 'Playlist'
        verbose_name_plural = 'Playlists'
        app_label = 'maio'
        db_table_comment = 'Contains the Playlists for Media.'
        get_latest_by = ['-date_modified']
        # order_with_respect_to = ['user', 'date_added']
        ordering = ['-date_modified']
        # indexes = [
        #     Index(fields=('sort', 'name', 'is_default', 'date_added', '-date_modified'))
        # ]


class Playlist(Model, metaclass=PlaylistMeta):
    '''Playlist model.'''
    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    media: ManyToManyField[Media, Playlist] = ManyToManyField(Media)
    name = CharField(max_length=1024)
    tn_path = CharField(max_length=1024)
    default_order = PositiveSmallIntegerField(default=0) # 0 random, 1 descending, 2 ascending
    seconds_between = FloatField(default=5.0)
    caption_type = ForeignKey(to=MaioMapType, on_delete=DO_NOTHING, default=MaioMapType.default)
    caption = TextField(null=True, blank=True)
    date_added = DateTimeField(auto_now_add=True)
    date_modified = DateTimeField(auto_now=True)
