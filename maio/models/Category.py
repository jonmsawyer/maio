'''
File: Category.py

Module: ``maio.models.Category``
'''

from __future__ import annotations
# from typing import Any

# import os
import uuid

# from django.conf import settings
from django.db.models import (
    Model, UUIDField, CharField, DateTimeField, IntegerField, BooleanField,
    ForeignKey, Index,
    CASCADE,
)
from django.db.models.base import ModelBase

# from conf import MaioConf


# maio_conf = MaioConf(config=settings.MAIO_SETTINGS)


class CategoryMeta(ModelBase):
    '''Metaclass for Category model.'''
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        app_label = 'maio'
        db_table_comment = 'Categories are ways to group Media.'
        get_latest_by = ['-date_modified']
        # order_with_respect_to = ['']
        ordering = ['-date_modified']
        indexes = [
            Index(fields=('sort', 'name', 'is_default', 'date_added', '-date_modified'))
        ]


class Category(Model, metaclass=CategoryMeta):
    '''File model. Represents a file stored in filestore/media.'''

    #: UUID unique ID
    id = UUIDField('UUID', primary_key=True, default=uuid.uuid4, editable=False)

    #: Maio User
    user = ForeignKey(to='MaioUser', on_delete=CASCADE)

    #: Sort order
    sort = IntegerField('Sort Order (0-9)', default=0)

    #: Is Default?
    is_default = BooleanField('Is Default?', default=False)

    #: Name
    name = CharField('Category', max_length=1024, default='Default Category')

    #: Date added
    date_added = DateTimeField(auto_now_add=True)

    #: Date modified
    date_modified = DateTimeField(auto_now=True)

    def __str__(self) -> str:
        id = str(self.id)[0:6]
        return f"[{id}] (Sort: {self.sort}) {self.name}"
