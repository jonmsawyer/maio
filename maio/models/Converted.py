'''
File: Converted.py

Module: ``maio.models.Converted``
'''

from __future__ import annotations

import uuid

from django.conf import settings
from django.db.models import (
    Model, UUIDField, ForeignKey, DateTimeField, PositiveIntegerField, DecimalField, FileField,
    CASCADE, DO_NOTHING,
)
from django.db.models.base import ModelBase
from django.utils.translation import gettext_lazy as _T

from conf import MaioConf


maio_conf = MaioConf(config=settings.MAIO_SETTINGS)

class ConvertedMeta(ModelBase):
    '''Metaclass for Converted model.'''
    class Meta:
        verbose_name = 'Converted File'
        verbose_name_plural = 'Converted Files'
        app_label = 'maio'
        db_table_comment = 'Converted Files.'
        get_latest_by = ['-date_modified']
        # order_with_respect_to = ['user', '-date_modified']
        ordering = ['-date_modified']
        # indexes = [
        #     Index(fields=('sort', 'name', 'is_default', 'date_added', '-date_modified'))
        # ]


class Converted(Model, metaclass=ConvertedMeta):
    '''Converteds model.'''
    id = UUIDField(_T('UUID'), primary_key=True, default=uuid.uuid4, editable=False)
    file = ForeignKey(to='File', on_delete=CASCADE)
    mime_type = ForeignKey(to='MaioMimeType', on_delete=DO_NOTHING)
    content_file = FileField(_T('Content File'), max_length=1024, upload_to=maio_conf.get_chain('converted', 'directory'))
    size = PositiveIntegerField(_T('Size (Bytes)'))
    width = PositiveIntegerField(_T('Width (Pixels)'))
    height = PositiveIntegerField(_T('Height (Pixels)'))
    length = DecimalField('Length (seconds)', max_digits=22, decimal_places=15)
    date_added = DateTimeField(_T('Date Added'), auto_now_add=True, editable=False)
    date_modified = DateTimeField(_T('Date Modified'), auto_now=True, editable=False)

    def __str__(self) -> str:
        return f"[{str(self.id)[0:6]}] - ({self.file}) - {self.mime_type}" # type: ignore
