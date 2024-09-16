'''
File: Caption.py

Module: ``maio.models.Caption``
'''

from __future__ import annotations
from typing import Any

import uuid

from django.db.models import (
    Model, UUIDField, ForeignKey, DateTimeField, BooleanField,
    CASCADE,
)
from django.db.models.base import ModelBase
from django.utils.translation import gettext_lazy as _T
from django.utils.safestring import mark_safe

from .MaioUser import MaioUser
from .MaioMapType import MaioMapTypeChoices # MaioMapType


USER_SETTINGS: dict[str, Any] = {
    'display_thumbnails_only': {
        'maio_type': MaioMapTypeChoices.BOOL,
        'default': False,
        'help': mark_safe(
            'Display only thumbnails in the Dashboard. Setting this option to <code>True</code> '
            'will hide media details in the Dashboard view.'
        ),
    }
}

class UserSettingMeta(ModelBase):
    '''Metaclass for Caption model.'''
    name = 'User Setting'
    verbose_name = 'User Settings'
    app_label = 'maio'
    db_table_comment = 'User system-wide settings.'
    get_latest_by = ['user', '-date_added']
    order_with_respect_to = ['user', '-date_added']
    ordering = ['media', 'caption_date']

class UserSetting(Model, metaclass=UserSettingMeta):
    '''UserSettings model.'''
    id = UUIDField(_T('UUID'), primary_key=True, default=uuid.uuid4, editable=False)
    user = ForeignKey(verbose_name=_T('Maio User'), to=MaioUser, on_delete=CASCADE)
    date_added = DateTimeField(_T('Date Added'), auto_now_add=True)
    display_thumbnails_only = BooleanField('Display Thumbnails Only', default=False)
    supress_warning_to_delete_media = BooleanField('Suppress Warning to Delete MEdia', default=False)

    # Non-model fields
    user_settings: dict[str, Any] = dict(USER_SETTINGS)

    def __str__(self) -> str:
        return f"[{str(self.id)[0:6]}] - ({self.user}) - {self.date_added}" # type: ignore
