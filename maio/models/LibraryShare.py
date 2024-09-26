'''
File: LibraryShare.py

Module: ``maio.models.LibraryShare``
'''

from __future__ import annotations
# from typing import Any

import uuid

from django.db.models import (
    Model, UUIDField, ForeignKey, DateTimeField, CharField,
    CASCADE,
)
from django.db.models.base import ModelBase
from django.utils.translation import gettext_lazy as _T

from .MaioUser import MaioUser
from .choices import PermissionChoices




class LibraryShareMeta(ModelBase):
    '''Metaclass for Caption model.'''
    class Meta:
        verbose_name = 'Library Share'
        verbose_name_plural = 'Library Shares'
        app_label = 'maio'
        db_table_comment = 'Library sharing between two Maio Users.'
        get_latest_by = ['-date_modified']
        # order_with_respect_to = ['user', '-date_modified']
        ordering = ['-date_modified']
        # indexes = [
        #     Index(fields=('sort', 'name', 'is_default', 'date_added', '-date_modified'))
        # ]
        unique_together = ('from_user', 'to_user')


class LibraryShare(Model, metaclass=LibraryShareMeta):
    '''LibraryShare model.'''
    id = UUIDField(_T('UUID'), primary_key=True, default=uuid.uuid4, editable=False)
    from_user = ForeignKey(verbose_name=_T('From Maio User'), to=MaioUser, on_delete=CASCADE, related_name='from_user')
    to_user = ForeignKey(verbose_name=_T('To Maio User'), to=MaioUser, on_delete=CASCADE, related_name='to_user')
    permission = CharField(_T('Permissions'), default='denied', choices=PermissionChoices.choices)
    date_added = DateTimeField(_T('Date Added'), auto_now_add=True, editable=False)
    date_modified = DateTimeField(_T('Date Modified'), auto_now=True, editable=False)

    def __str__(self) -> str:
        return f"[{str(self.id)[0:6]}] ({self.permission}) From: {self.from_user} - To: {self.to_user}" # type: ignore
