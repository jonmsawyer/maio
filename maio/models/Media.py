'''
File: Media.py

Module: ``maio.models.Media``
'''

from __future__ import annotations

import uuid

from django.http import HttpRequest
from django.db.models import (
    Model, UUIDField, ForeignKey, ManyToManyField, CharField, FloatField, PositiveIntegerField,
    DateTimeField, BooleanField, URLField, TextField, QuerySet, CASCADE, DO_NOTHING,
)
from django.db.models.base import ModelBase
from django.contrib.auth.models import User

from .File import File
from .Tag import Tag
from .MaioType import MaioType, MaioTypeChoices
from .MaioMapType import MaioMapType


class MediaMeta(ModelBase):
    '''Metaclass for Media model.'''
    name = 'Media'
    verbose_name = 'Media'
    app_label = 'maio'
    db_table_comment = 'More than one Media may map onto one File.'
    get_latest_by = ['file', '-date_modified']
    order_with_respect_to = ['file', '-date_modified']


class Media(Model, metaclass=MediaMeta):
    '''
    Media model. Represents a sort of Meta object for a given File. Files may
    have many Media, but there's at least one Media per File is that File's
    ``media_class`` is ``image``.
    '''

    #: UUID unique ID.
    id = UUIDField('UUID', primary_key=True, default=uuid.uuid4, editable=False)

    #: The File that this Media points to.
    file = ForeignKey(File, on_delete=CASCADE)

    #: The Maio Type of this Media.
    maio_type = ForeignKey(to=MaioType, on_delete=DO_NOTHING, default=MaioType.default)

    #: Owner of the File
    owner = ForeignKey(User, on_delete=CASCADE)

    #: The media's tags
    tags: ManyToManyField[Tag, Media] = ManyToManyField(Tag)

    #: The base name for the File.
    name = CharField('Name', max_length=1024)

    #: The File extension, if known.
    extension = CharField('Extension', max_length=8, null=True, blank=True)

    #: The date time when this File was added to Maio.
    date_added = DateTimeField('Date Added', auto_now_add=True)

    #: The date time when this File was modified by Maio.
    date_modified = DateTimeField('Date Modified', auto_now=True)

    #: The width in pixels of the Media
    width = PositiveIntegerField('Width (Pixels)', null=True, blank=True)

    #: The height in pixes of the Media
    height = PositiveIntegerField('Height (Pixels)', null=True, blank=True)

    #: The thumbnail width
    tn_width = PositiveIntegerField('Thumbnail Width (Pixels)', null=True, blank=True)

    #: The thumbnail height
    tn_height = PositiveIntegerField('Thumbnail Height (Pixels)', null=True, blank=True)

    #: The length (in milliseconds for Audio or Video, null for Image and Document)
    length = FloatField('Length (Milliseconsd)', null=True, blank=True)

    #: The author of this Media, if there is one.
    author = CharField('Author', max_length=1024, null=True, blank=True)

    #: The URL source of this Media, if there is one.
    url = URLField('URL', max_length=1024, null=True, blank=True)

    #: The text source of this Media, if there is one.
    source = CharField('Source', max_length=1024, null=True, blank=True)

    #: The Copyright info of this Media, if there is one.
    copyright = CharField('Copyright', max_length=1024, null=True, blank=True)

    #: Comment type
    comment_type = ForeignKey(to=MaioMapType, on_delete=DO_NOTHING, default=MaioMapType.default)

    #: Some image formats store other meta data in the file, such as GPS location,
    #: lense information, type of camera, etc. What doesn't fit neatly into the
    #: fields above, goes into the ``comments`` field. Can be set to ``None``.
    comment = TextField('Comment', null=True, blank=True)

    #: Set to ``True`` to mark this File "active". An active File means that the File is
    #: searchable and is a valid file to include in Playlists, etc. A non-active File is
    #: hidden from the regular views and filters.
    #:
    #: Default: ``True``
    is_active = BooleanField('Is Active?', default=True)

    #: Set to ``True`` to mark this File as hidden. Only the owner of the File can see the
    #: File. Set to ``False`` to show this file in default views and filters.
    #:
    #: Default: ``False``
    is_hidden = BooleanField('Is Hidden?', default=False)

    #: Set to ``True`` if this File shall be marked for deletion. Akin to the Recycle Bin
    #: in Windows. Set to ``False`` to prevent this File from getting deleted.
    #:
    #: Default: ``False``
    is_deleted = BooleanField('Is Deleted?', default=False)

    def __str__(self) -> str:
        id = str(self.id)[0:6]
        maio_type = self.file.maio_type
        name = self.name
        if self.extension:
            ext = '.'+self.extension
        else:
            ext = ''
        size = self.file.size
        return f"({id}) [{maio_type}] {name}{ext} - {size} bytes"

    @staticmethod
    def get_all_images(request: HttpRequest) -> QuerySet[Media]:
        return Media.objects.filter(
            owner=request.user,
            maio_type=MaioType.objects.get(maio_type=MaioTypeChoices.IMAGE),
            is_active=True,
            is_hidden=False,
            is_deleted=False
        )
