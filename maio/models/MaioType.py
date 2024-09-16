'''
File: File.py

Module: ``maio.models.File``
'''

from __future__ import annotations

import uuid
from uuid import UUID

from django.db.models import (
    Model, UUIDField, CharField, TextChoices,
)
from django.db.models.base import ModelBase
# from django.db import IntegrityError
from django.utils.translation import gettext_lazy as _T


class MaioTypeChoices(TextChoices):
    '''Enumerated text choices for `File` model's `maio_type` field.'''
    IMAGE = 'image', _T('Image')
    AUDIO = 'audio', _T('Audio')
    VIDEO = 'video', _T('Video')
    DOCUMENT = 'document', _T('Document')
    OTHER = 'other', _T('Other')


class MaioTypeMeta(ModelBase):
    '''Metaclass for MaioType model.'''
    name = 'Maio Type'
    verbose_name = 'Maio Types'
    app_label = 'maio'
    db_table_comment = 'General Maio Types.'
    # get_latest_by = ['-date_modified']
    # order_with_respect_to = ['']
    ordering = ['maio_type']


class MaioType(Model, metaclass=MaioTypeMeta):
    '''MaioType model.'''
    id = UUIDField('UUID', primary_key=True, default=uuid.uuid4, editable=False)
    maio_type = CharField('Maio Type', max_length=20, choices=MaioTypeChoices.choices, unique=True)

    def __str__(self) -> str:
        return self.maio_type

    @staticmethod
    def default() -> UUID:
        '''Return the defau't MaioType.'''
        MaioType.objects.get_or_create(maio_type=MaioTypeChoices.IMAGE)
        MaioType.objects.get_or_create(maio_type=MaioTypeChoices.AUDIO)
        MaioType.objects.get_or_create(maio_type=MaioTypeChoices.VIDEO)
        MaioType.objects.get_or_create(maio_type=MaioTypeChoices.DOCUMENT)
        maio_type, _created = MaioType.objects.get_or_create(maio_type=MaioTypeChoices.OTHER)
        return maio_type.id

    def get_choice(self) -> MaioTypeChoices:
        '''Get the Maio Type Choice for this MaioType.'''
        if self.maio_type == 'image':
            return MaioTypeChoices.IMAGE
        elif self.maio_type == 'audio':
            return MaioTypeChoices.AUDIO
        elif self.maio_type == 'video':
            return MaioTypeChoices.VIDEO
        elif self.maio_type == 'document':
            return MaioTypeChoices.DOCUMENT
        return MaioTypeChoices.OTHER
