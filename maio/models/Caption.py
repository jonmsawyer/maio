'''
File: Caption.py

Module: ``maio.models.Caption``
'''

from __future__ import annotations

import uuid

from django.db.models import (
    Model, UUIDField, ForeignKey, CharField, URLField, DateTimeField, TextField,
    CASCADE, DO_NOTHING,
)
from django.db.models.base import ModelBase

from .Media import Media
from .MaioMapType import MaioMapType, MaioMapTypeChoices


class CaptionMeta(ModelBase):
    '''Metaclass for Caption model.'''
    name = 'Caption'
    verbose_name = 'Captions'
    app_label = 'maio'
    db_table_comment = 'Captions are attached to Media.'
    get_latest_by = ['media', '-caption_date']
    order_with_respect_to = ['media', 'caption_date']
    # ordering = ['media', 'caption_date']

class Caption(Model, metaclass=CaptionMeta):
    '''Caption model.'''
    id = UUIDField('UUID', primary_key=True, default=uuid.uuid4, editable=False)
    media = ForeignKey(Media, on_delete=CASCADE)
    author = CharField('Author', max_length=1024, null=True, blank=True)
    url = URLField('URL', max_length=1024, null=True, blank=True)
    date_added = DateTimeField('Date Added', auto_now_add=True)
    date_modified = DateTimeField('Date Modified', auto_now=True)
    caption_date = DateTimeField('Caption Date', null=True, blank=True)
    caption_type = ForeignKey(
        to=MaioMapType,
        on_delete=DO_NOTHING,
        default=MaioMapType.default,
    )
    caption = TextField('Caption')

    def __str__(self):
        return f"{self.media.name} - {self.caption_date} - {self.caption[0:20]}"
