'''
File: Love.py

Module: ``maio.models.Love``
'''

from __future__ import annotations

import uuid

from django.db.models import Model, UUIDField, DateTimeField, ForeignKey, CASCADE
from django.db.models.base import ModelBase


class LoveMeta(ModelBase):
    '''Metaclass for Love model.'''
    class Meta:
        verbose_name = 'Love'
        verbose_name_plural = 'Loves'
        app_label = 'maio'
        db_table_comment = 'Contains the Loves for Media.'
        get_latest_by = ['-date_modified']
        # order_with_respect_to = ['user', 'date_added']
        ordering = ['-date_modified']
        # indexes = [
        #     Index(fields=('sort', 'name', 'is_default', 'date_added', '-date_modified'))
        # ]


class Love(Model, metaclass=LoveMeta):
    '''Love model.'''
    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = ForeignKey(to='MaioUser', on_delete=CASCADE)
    media = ForeignKey(to='Media', on_delete=CASCADE)
    date_added = DateTimeField(auto_now_add=True)
    date_modified = DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.media.owner} loves {self.media}"
