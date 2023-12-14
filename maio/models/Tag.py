'''
File: Tag.py

Module: ``maio.models.Tag``
'''

from __future__ import annotations

import uuid

from django.db.models import Model, UUIDField, CharField, DateTimeField
from django.db.models.base import ModelBase


class TagMeta(ModelBase):
    '''Metaclass for Tag model.'''
    ordering = ['name']


class Tag(Model, metaclass=TagMeta):
    '''Tag model.'''
    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = CharField(max_length=255, unique=True)
    date_added = DateTimeField(auto_now_add=True)
    date_modified = DateTimeField(auto_now=True)

    def __str__(self):
        return '({}) {}'.format(str(self.id)[:6], self.name)
