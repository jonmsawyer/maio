'''
File: Collection.py

Module: ``maio.models.Collection``
'''

from __future__ import annotations
from typing import Optional

import uuid

from django.http import HttpRequest
from django.db.models import (
    Model, UUIDField, CharField, DateTimeField, IntegerField, BooleanField,
    ForeignKey, Index,
    CASCADE, DO_NOTHING,
)
from django.db.models.base import ModelBase
from django.db.models.manager import BaseManager


class CollectionMeta(ModelBase):
    '''Metaclass for Collection model.'''
    class Meta:
        verbose_name = 'Collection'
        verbose_name_plural = 'Collections'
        app_label = 'maio'
        db_table_comment = 'Collections are ways to group Media.'
        get_latest_by = ['-date_modified']
        # order_with_respect_to = ['']
        ordering = ['sort', 'date_added']
        indexes = [
            Index(fields=('sort', 'name', 'is_default', 'date_added', '-date_modified'))
        ]
        unique_together = ['parent', 'name']


class Collection(Model, metaclass=CollectionMeta):
    '''File model. Represents a file stored in filestore/media.'''

    #: UUID unique ID
    id = UUIDField('UUID', primary_key=True, default=uuid.uuid4, editable=False)

    #: Parent Collection UUID
    parent = ForeignKey(to='Collection', on_delete=CASCADE, null=True, blank=True)

    #: Maio User
    user = ForeignKey(to='MaioUser', on_delete=CASCADE)

    #: Sort order
    sort = IntegerField('Sort Order (0-9)', default=0)

    #: Is Default?
    is_default = BooleanField('Is Default?', default=False)

    #: Is Favorite?
    is_favorite = BooleanField('Is Favorite?', default=False)

    #: Name
    name = CharField('Collection Name', max_length=1024, default='Default Collection')

    #: Thumbnail
    thumbnail = ForeignKey(to='Thumbnail', on_delete=DO_NOTHING, null=True, blank=True)

    #: Date added
    date_added = DateTimeField(auto_now_add=True)

    #: Date modified
    date_modified = DateTimeField(auto_now=True)

    def __str__(self) -> str:
        id = str(self.id)[0:6]
        parent_name: Optional[str] = None
        if self.parent:
            parent_name = self.parent.name
        return f"[{parent_name} -> {id}] {self.sort}: {self.name}"

    @staticmethod
    def get_list(
        request: HttpRequest,
        parent_id: Optional[str] = None,
    ) -> BaseManager[Collection]:
        '''Get a list of child Collections underneath this one.'''
        if parent_id:
            return (
                Collection.objects
                    .get(id=parent_id, user=request.maio_user)
                    .collection_set.all()
            )
        return Collection.objects.filter(parent=None, user=request.maio_user)
