'''
File: MaioMap.py

Module: ``maio.models.MaioMap``
'''

from __future__ import annotations
from typing import Any

import uuid

from django.http import HttpRequest
from django.db.models import (
    Model, UUIDField, CharField, DateTimeField, TextField, BooleanField, ForeignKey,
    CASCADE, DO_NOTHING,
)
from django.db.models.base import ModelBase
from django.utils.translation import gettext_lazy as _T

from .MaioUser import MaioUser
from .MaioMapType import MaioMapType


class MaioMapMeta(ModelBase):
    '''Metaclass for MaioMap model.'''
    class Meta:
        verbose_name = 'Maio Map'
        verbose_name_plural = 'Maio Map'
        app_label = 'maio'
        db_table_comment = 'Maio Map maps types to values.'
        get_latest_by = ['-date_modified']
        # order_with_respect_to = ['user', 'key']
        ordering = ['-date_modified']
        # indexes = [
        #     Index(fields=('sort', 'name', 'is_default', 'date_added', '-date_modified'))
        # ]


class MaioMap(Model, metaclass=MaioMapMeta):
    '''
    MaioMap model.

    Represents Maio configuration in the form of key->value pairs where values have defined
    types and is validated before saving to the database.
    '''
    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = ForeignKey(to=MaioUser, on_delete=CASCADE, default=MaioUser.default)
    type = ForeignKey(to=MaioMapType, on_delete=DO_NOTHING, default=MaioMapType.default)
    key = CharField(_T('Key'), max_length=254, unique=True)
    value = TextField(_T('Value'), null=True, blank=True)
    allow_null = BooleanField(_T('Allow Null?'), default=False)
    is_enabled = BooleanField(_T('Is Enabled?'), default=True)
    date_added = DateTimeField(_T('Insert DateTime'), auto_now_add=True)
    date_modified = DateTimeField(_T('Updated DateTime'), auto_now=True)

    def __str__(self):
        return f"{self.key} -> ({self.type.maio_map_type}) `{self.value[0:20] if self.value else None}`"

    @staticmethod
    def get(request: HttpRequest, key: str) -> dict[str, str] | None:
        return None

    @staticmethod
    def set(request: HttpRequest, key: str, value: Any | None) -> bool:
        return False
