'''
File: Thumbnail.py

Module: ``maio.models.Thumbnail``
'''

from __future__ import annotations
from typing import Any

import uuid

from django.conf import settings
from django.db.models import (
    Model, UUIDField, CharField, DateTimeField, FileField, PositiveIntegerField, ForeignKey, Index,
    CASCADE,
)
from django.db.models.base import ModelBase

from conf import MaioConf


maio_conf = MaioConf(config=settings.MAIO_SETTINGS)


class ThumbnailMeta(ModelBase):
    '''Metaclass for File model.'''
    class Meta:
        verbose_name = 'Thumbnail'
        verbose_name_plural = 'Thumbnails'
        app_label = 'maio'
        db_table_comment = 'Thumbnails are saved to the hard drive, network, or cloud.'
        get_latest_by = ['-date_modified']
        # order_with_respect_to = ['']
        ordering = ['-date_modified']
        indexes = [
            Index(fields=('date_added', '-date_modified'))
        ]


class Thumbnail(Model, metaclass=ThumbnailMeta):
    '''File model. Represents a file stored in filestore/media.'''

    #: UUID unique ID.
    id = UUIDField('UUID', primary_key=True, default=uuid.uuid4, editable=False)

    #: The File for this Thumbnail.
    file = ForeignKey(to='File', on_delete=CASCADE)

    #: The md5sum hash of the File, should be unique.
    md5sum = CharField('MD5 Sum', max_length=32, unique=True, editable=False)

    #: The File path stored in ./filestore/media/
    content_file = FileField('Content File', max_length=1024, upload_to=maio_conf.get_chain('meta', 'directory'))

    #: The thumbnail extension.
    extension = CharField('Extension', max_length=8, default='jpg')

    #: The URI of the thumbnail relative to `settings.STATIC_URL`
    uri = CharField('URI', max_length=1024, default=maio_conf.get_static_media_uri())

    #: Width
    width = PositiveIntegerField('Width')

    #: Height
    height = PositiveIntegerField('Height')

    #: Size
    size = PositiveIntegerField('Size (Bytes)')

    #: Date added
    date_added = DateTimeField(auto_now_add=True)

    #: Date modified
    date_modified = DateTimeField(auto_now=True)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.content_file.field.upload_to = maio_conf.get_chain('meta', 'directory')

    def __str__(self) -> str:
        id = str(self.id)[0:6]
        return f"({id}) {self.content_file.path}"
