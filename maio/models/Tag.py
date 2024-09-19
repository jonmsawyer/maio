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
    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        app_label = 'maio'
        db_table_comment = 'Contains the Tags for Media.'
        get_latest_by = ['-date_modified']
        # order_with_respect_to = ['user', 'date_added']
        ordering = ['name']
        # indexes = [
        #     Index(fields=('sort', 'name', 'is_default', 'date_added', '-date_modified'))
        # ]


class Tag(Model, metaclass=TagMeta):
    '''Tag model.'''
    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = CharField(max_length=255, unique=True)
    date_added = DateTimeField(auto_now_add=True)
    date_modified = DateTimeField(auto_now=True)

    def __str__(self):
        return '({}) {}'.format(str(self.id)[:6], self.name)
