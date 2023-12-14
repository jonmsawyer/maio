'''
File: KeyValue.py

Module: ``maio.models.KeyValue``
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
    '''Metaclass for Map model.'''
    name = 'Maio User'
    verbose_name = 'Maio Users'
    app_label = 'maio'
    db_table_comment = 'Maio users are also Django users.'
    get_latest_by = ['user', '-upd_dttm']
    order_with_respect_to = ['user', 'key']
    # ordering = ['user', 'key']


class MaioMap(Model, metaclass=MaioMapMeta):
    '''
    MaioMap model.

    Represents Maio configuration in the form of key->value pairs where values have defined
    types and is validated before saving to the database.
    '''
    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = ForeignKey(to=MaioUser, on_delete=CASCADE, default=MaioUser.default)
    type = ForeignKey(to=MaioMapType, on_delete=DO_NOTHING, default=MaioMapType.default)
    key = CharField('Key', max_length=254, unique=True)
    value = TextField('Value', null=True, blank=True)
    allow_null = BooleanField('Allow Null?', default=False)
    is_enabled = BooleanField('Is Enabled?', default=True)
    ins_dttm = DateTimeField('Insert DateTime', auto_now_add=True)
    upd_dttm = DateTimeField('Updated DateTime', auto_now=True)

    def __str__(self):
        return f"{self.key} -> ({self.type.maio_map_type}) `{self.value[0:20] if self.value else None}`"

    @staticmethod
    def get(request: HttpRequest, key: str) -> dict[str, str] | None:
        # try:
        #     return Map.objects.filter(key=key).values()
        # except IndexError:
        #     return None
        return None

    @staticmethod
    def set(request: HttpRequest, key: str, value: Any | None) -> bool:
        return False
