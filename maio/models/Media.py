'''
File: Media.py

Module: ``maio.models.Media``
'''

from __future__ import annotations

import os
import uuid
import subprocess

from django.conf import settings
from django.http import HttpRequest
from django.core.files.uploadedfile import UploadedFile
from django.db.models import (
    Model, UUIDField, ForeignKey, ManyToManyField, CharField, FloatField, PositiveIntegerField,
    DateTimeField, BooleanField, URLField, TextField, QuerySet, CASCADE, DO_NOTHING,
)
from django.db.models.base import ModelBase
from django.contrib.auth.models import User

from conf import MaioConf
from maio import filestore as fs

# from maio import filestore as fs

from .File import File
from .Tag import Tag
from .MaioType import MaioType, MaioTypeChoices
from .MaioMapType import MaioMapType
from .MaioMimeType import MaioMimeType


maio_conf = MaioConf(config=settings.MAIO_SETTINGS)

class StaticMediaURINotSetError(Exception):
    '''Raise this error when the static media URI is not set.'''

class StaticThumbnailURINotSetError(Exception):
    '''Raise this error when the static thumbnail URI is not set.'''

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
    file = ForeignKey(to=File, on_delete=CASCADE)

    #: Owner of the File
    owner = ForeignKey(to=User, on_delete=DO_NOTHING)

    #: The media's tags
    tags: ManyToManyField[Tag, Media] = ManyToManyField(Tag)

    #: The base name for the File.
    name = CharField('Name', max_length=1024)

    #: The File extension, if known.
    extension = CharField('Extension', max_length=8, null=True, blank=True)

    #: The Thumbnail extension, if known.
    tn_extension = CharField('Thumbnail Extension', max_length=8, null=True, blank=True)

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

    #: Set to ``True`` to mark this File as hidden. Only the owner of the File can see the
    #: File. Set to ``False`` to show this file in default views and filters.
    #:
    #: Default: ``False``
    is_public = BooleanField('Is Public?', default=False)

    #: Set to ``True`` if this File shall be marked for deletion. Akin to the Recycle Bin
    #: in Windows. Set to ``False`` to prevent this File from getting deleted.
    #:
    #: Default: ``False``
    is_deleted = BooleanField('Is Deleted?', default=False)

    def __str__(self) -> str:
        id = str(self.id)[0:6]
        maio_type = self.file.mime_type.maio_type
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
            file__mime_type__in=MaioMimeType.objects.filter(
                maio_type__in=MaioType.objects.filter(maio_type=MaioTypeChoices.IMAGE)
            ),
            is_active=True,
            is_hidden=False,
            is_deleted=False
        )

    @staticmethod
    def get_all_media(request: HttpRequest) -> QuerySet[Media]:
        return Media.objects.filter(
            owner=request.user,
            # file__mime_type__in=MaioMimeType.objects.filter(
            #     maio_type__in=MaioType.objects.filter(maio_type=MaioTypeChoices.IMAGE)
            # ),
            is_active=True,
            is_hidden=False,
            is_deleted=False
        )

    @staticmethod
    def create_from_maio_file(
        request: HttpRequest,
        maio_file: File,
        content_file: UploadedFile,
    ) -> Media:
        '''Create a new Media record for the given File and UploadedFile.'''
        name = '.'.join(content_file.name.split('.')[:-1])
        extension = ''.join(content_file.name.split('.')[-1])
        width = None
        height = None
        tn_extension = 'jpg'
        if maio_file.mime_type.get_maio_type_choice() == MaioTypeChoices.IMAGE:
            image, _image_path = maio_file.load_image()
            width = image.width
            height = image.height
            image.close()
            tn_extension = extension
        if maio_file.mime_type.get_maio_type_choice() == MaioTypeChoices.VIDEO:
            # TODO: Process video height and width
            video_path = os.path.join(fs.mk_md5_dir_media(maio_file.md5sum), maio_file.get_filename())
            ffprobe_cmd = [
                maio_conf.get_ffprobe_bin_path(),
                "-v", "error",
                "-select_streams", "v",
                "-show_entries", "stream=width,height",
                "-of", "csv=p=0:s=x",
                video_path,
            ]
            try:
                output = subprocess.run(ffprobe_cmd, capture_output=True)
                output = str(output.stdout, encoding='UTF-8')
                width = output.split('x')[0]
                height = output.split('x')[1]
            except subprocess.CalledProcessError:
                raise

        maio_file.process_thumbnail()

        # _deets = f'''
        #     Name: {name}
        #     Extension: {extension}
        #     Width: {width}
        #     Height: {height}
        #     Maio File: {maio_file}
        #     Content File: {content_file}
        # '''
        # raise Exception(_deets)

        return Media.objects.create(
            file=maio_file,
            owner=request.user,
            name=name,
            extension=extension,
            tn_extension=tn_extension,
            width=width,
            height=height,
            tn_width=maio_file.thumbnail.width,
            tn_height=maio_file.thumbnail.height,
        )

    def get_static_media_uri(self) -> str | None:
        '''Get the static URL of this resource.'''
        # static_uri = settings.STATIC_URL
        # media_path = settings.MAIO_SETTINGS.get('media', {'directory': 'media'}).get('directory')
        static_uri = maio_conf.get_static_media_uri()
        if not static_uri:
            raise StaticMediaURINotSetError(
                'Static Media URI must be set. See settings.MAIO_SETTINGS'
            )
        return f"{static_uri}{self.get_media_path()}"

    def get_static_thumbnail_uri(self) -> str | None:
        '''Get the static URL of this resource.'''
        static_uri = maio_conf.get_static_thumbnail_uri()
        if not static_uri:
            raise StaticThumbnailURINotSetError(
                'Static Thumbnail URI must be set. See settings.MAIO_SETTINGS'
            )
        return f"{static_uri}{self.get_thumbnail_path()}"

    def get_media_path(self) -> str:
        '''Get the media's relative path.'''
        md5sum = self.file.md5sum
        extension = self.extension
        level_one = md5sum[0:2]
        level_two = md5sum[2:4]
        return f"{level_one}/{level_two}/{md5sum}.{extension}"

    def get_thumbnail_path(self) -> str:
        '''Get the media's relative path.'''
        md5sum = self.file.md5sum
        extension = self.tn_extension if self.tn_extension else self.extension
        level_one = md5sum[0:2]
        level_two = md5sum[2:4]
        return f"{level_one}/{level_two}/{md5sum}.{extension}"
