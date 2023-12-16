'''
File: File.py

Module: ``maio.models.File``
'''

from __future__ import annotations

import uuid

from django.db.models import (
    Model, UUIDField, CharField, DO_NOTHING,
)
from django.db.models.base import ModelBase

from .MaioType import MaioType


class MaioMimeTypeMeta(ModelBase):
    '''Metaclass for MaioType model.'''
    name = 'Maio Mime Type'
    verbose_name = 'Maio Mime Types'
    app_label = 'maio'
    db_table_comment = 'General Maio Mime Types.'
    # get_latest_by = ['-date_modified']
    # order_with_respect_to = ['']
    ordering = ['mime_type']


class MaioMimeType(Model, metaclass=MaioMimeTypeMeta):
    '''MaioType model.'''
    id = UUIDField('UUID', primary_key=True, default=uuid.uuid4, editable=False)
    maio_type = ForeignKey(to=MaioType, on_delete=DO_NOTHING, default=MaioType.default)
    mime_type = CharField('Mime Type', max_length=254)
    extensions = CharField('Extensions', max_length=254, null=True, blank=True)

    def __str__(self) -> str:
        return self.mime_type
