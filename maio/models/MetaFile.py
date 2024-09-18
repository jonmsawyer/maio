'''
File: MetaFile.py

Module: ``maio.models.MetaFile``
'''

from __future__ import annotations
from typing import Any

import uuid

from django.conf import settings
from django.db.models import (
    Model, UUIDField, CharField, DateTimeField, FileField, ForeignKey, Index, CASCADE,
)
from django.db.models.base import ModelBase

from conf import MaioConf


maio_conf = MaioConf(config=settings.MAIO_SETTINGS)


class MetaFileMeta(ModelBase):
    '''Metaclass for File model.'''
    name = 'MetaFile'
    verbose_name = 'MetaFiles'
    app_label = 'maio'
    db_table_comment = 'MetaFiles are saved to the hard drive, network, or cloud.'
    get_latest_by = ['-date_modified']
    # order_with_respect_to = ['']
    ordering = ['-date_modified']
    indexes = [
        Index(fields=('content_file', 'date_added', '-date_modified')),
    ]


class MetaFile(Model, metaclass=MetaFileMeta):
    '''File model. Represents a file stored in filestore/meta.'''

    #: UUID unique ID.
    id = UUIDField('UUID', primary_key=True, default=uuid.uuid4, editable=False)

    #: The file for this Meta file.
    file = ForeignKey(to='File', on_delete=CASCADE)

    #: The md5sum hash of the File, should be unique.
    md5sum = CharField('MD5 Sum', max_length=32, unique=True, editable=False)

    #: The File path stored in ./filestore/media/
    content_file = FileField('Meta File', max_length=1024)

    #: Date added
    date_added = DateTimeField(auto_now_add=True)

    #: Date modified
    date_modified = DateTimeField(auto_now=True)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.content_file.field.upload_to = maio_conf.get_meta_directory()

    def __str__(self) -> str:
        id = str(self.id)[0:6]
        return f"({id}) {self.content_file.path}"
