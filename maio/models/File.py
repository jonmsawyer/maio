'''
File: File.py

Module: ``maio.models.File``
'''

from __future__ import annotations

# import os
import uuid
import hashlib

import magic # for mime types

from django.conf import settings
from django.db.models import (
    Model, UUIDField, CharField, PositiveIntegerField, FloatField, DateTimeField, ForeignKey,
    FileField, ImageField, DO_NOTHING,
)
from django.db.models.base import ModelBase
from django.utils.datastructures import MultiValueDictKeyError


from conf import MaioConf
from .maiofields import FixedCharField
from .MaioType import MaioType


maio_conf = MaioConf(settings.MAIO_SETTINGS)


class MimeTypeNotSetError(Exception):
    '''Raise this error when the `mime_type` field is not set.'''


class FileMeta(ModelBase):
    '''Metaclass for File model.'''
    name = 'File'
    verbose_name = 'Files'
    app_label = 'maio'
    db_table_comment = 'Files are saved to the hard drive, network, or cloud.'
    get_latest_by = ['-date_modified']
    # order_with_respect_to = ['']
    ordering = ['-date_modified']


class File(Model, metaclass=FileMeta):
    '''File model. Represents a file stored in filestore/media.'''

    #: UUID unique ID.
    id = UUIDField('UUID', primary_key=True, default=uuid.uuid4, editable=False)

    #: Maio's type.
    maio_type = ForeignKey(to=MaioType, on_delete=DO_NOTHING)

    #: The md5sum hash of the File, should be unique.
    md5sum = FixedCharField('MD5SUM', max_length=32, unique=True, editable=False)

    #: The base name for the File.
    original_name = CharField('Original Name', max_length=1024, editable=False)

    #: The File extension, if known.
    original_extension = CharField('Original Extension', max_length=8, null=True, blank=True, editable=False)

    #: The File's mime type.
    mime_type = CharField('MIME Type', max_length=64, editable=False)

    #: The size, in bytes, of the File.
    size = PositiveIntegerField('Size (Bytes)', default=0, editable=False)

    #: File modified date, as a Unix time stamp.
    mtime = FloatField('Modified Time', default=0.0, editable=False)

    #: The thumbnail path stored in ./filestore/thumbnails/.
    thumbnail = ImageField('Thumbnail File', max_length=1024, upload_to=maio_conf.get_thumbnail_path(), null=True, blank=True, editable=False)

    #: The File path stored in ./filestore/media/
    content_file = FileField('Content File', max_length=1024, upload_to=maio_conf.get_upload_path(), null=True, blank=True)

    #: The META file path fored in ./filestore/media/
    meta_file = FileField('Meta File', max_length=1024, upload_to=maio_conf.get_meta_path(), null=True, blank=True, editable=False)

    #: The date time when this File was added to Maio.
    date_added = DateTimeField('Date Added', auto_now_add=True)

    #: The date time when this File was modified by Maio.
    date_modified = DateTimeField('Date Modified', auto_now=True)

    def __str__(self) -> str:
        id = str(self.id)[0:6]
        name = self.original_name
        ext = self.original_extension
        mime = self.mime_type
        size = self.size
        return f"({id}) {name}.{ext} - {mime} - {size} bytes"

    @staticmethod
    def handle_uploaded_file(request: HttpRequest, field: str) -> File | bool:
        '''Handle the uploaded file as given by `request.FILES`.'''
        try:
            content_file = request.FILES[field]
            maio_file = File(content_file=content_file)
        except MultiValueDictKeyError:
            return False

        _deets = f'''
            Content File
            ------------
            Name: {maio_file.content_file.name}
            Size: {maio_file.content_file.size}
            Content Type: {content_file.content_type}
            Content Type Extra: {content_file.content_type_extra}
            Charset: {content_file.charset}
            Upload To: {File.content_file.field.upload_to}
        '''
        # raise Exception(_deets)

        maio_file.save_file(request)
        maio_file.set_data(request, content_file)
        return maio_file

    def save_file(self):
        '''Save the file referenced by `self.content_file`.'''
        with open(self.content_file, 'wb+') as destination:
            for chunk in self.content_file.chunks():
                destination.write(chunk)

    def set_data(self, request: HttpRequest, content_file):
        '''Set the data attributes of this object based on the uploaded file and input data.'''
        self.md5sum = self.calculate_md5sum()
        self.original_name = ''.join(self.content_file.name.split('.')[:-1])
        self.original_extension = ''.join(self.content_file.name.split('.')[1:])
        self.mime_type = self.calculate_mimetype()
        self.maio_type = self.calculate_maio_type()

    def calculate_md5sum(self) -> str:
        '''Return the md5sum of the file represented by this object.'''
        return hashlib.md5(open(self.content_file, 'rb').read()).hexdigest

    def calculate_mimetype(self):
        '''Return the mime type of the file represented by this object.'''
        mime = magic.Magic(mime=True)
        return mime.from_file(self.content_file.path)

    def calculate_maio_type(self):
        '''Return the MaioType of the file represented by this object.'''
        if not self.mime_type:
            raise MimeTypeNotSetError(
                'The `mime_type` must be set in order to calculate the `MaioType`.'
            )

        return 
        # return MaioType(maio_type=MaioTypeChoices.IMAGE)
