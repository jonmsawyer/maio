'''
File: Slideshow.py

Module: ``maio.models.Slideshow``
'''

from __future__ import annotations

import uuid

from django.db.models import (
    Model, UUIDField, ForeignKey, DateTimeField, JSONField, PositiveSmallIntegerField,
    DecimalField,
    CASCADE,
)
from django.db.models.base import ModelBase
from django.utils.translation import gettext_lazy as _T


class SlideshowMeta(ModelBase):
    '''Metaclass for Slideshow model.'''
    class Meta:
        verbose_name = 'Slideshow'
        verbose_name_plural = 'Slideshows'
        app_label = 'maio'
        db_table_comment = 'Slideshow meta data for Files.'
        get_latest_by = ['-date_modified']
        # order_with_respect_to = ['user', '-date_modified']
        ordering = ['-date_modified']
        # indexes = [
        #     Index(fields=('sort', 'name', 'is_default', 'date_added', '-date_modified'))
        # ]


class Slideshow(Model, metaclass=SlideshowMeta):
    '''Slideshows model.'''
    id = UUIDField(_T('UUID'), primary_key=True, default=uuid.uuid4, editable=False)
    file = ForeignKey(to='File', on_delete=CASCADE)
    indexes: JSONField[str] = JSONField('Slideshow Indexes (list[float])')
    num_slices = PositiveSmallIntegerField('Number of Slices for Indexes')
    length = DecimalField('Length (seconds)', max_digits=22, decimal_places=15)
    date_added = DateTimeField(_T('Date Added'), auto_now_add=True, editable=False)
    date_modified = DateTimeField(_T('Date Modified'), auto_now=True, editable=False)

    def __str__(self) -> str:
        return f"[{str(self.id)[0:6]}] - ({self.file}) - {self.indexes}" # type: ignore
