'''
File: UserSetting.py

Module: ``maio.models.UserSetting``
'''

from __future__ import annotations
from typing import Any

import uuid

from django.db.models import (
    Model, UUIDField, ForeignKey, DateTimeField, CharField, BooleanField,
    CASCADE,
)
from django.db.models.base import ModelBase
from django.utils.translation import gettext_lazy as _T

from .MaioUser import MaioUser
from .MaioMapType import MaioMapTypeChoices


USER_SETTINGS: dict[str, Any] = {
    'maio_theme': {
        'name': _T('Maio Theme'),
        'maio_type': MaioMapTypeChoices.TEXT,
        'max_length': 50,
        'default': 'default',
        'choices': (
            ('default', _T('Default: standard Maio theme')),
        ),
        'help': _T(
            'Set the default Maio theme. '
            'This setting will affect how you experience Maio.'
        ),
    },
    'default_dashboard_view': {
        'name': _T('Default Dashboard View'),
        'maio_type': MaioMapTypeChoices.TEXT,
        'max_length': 50,
        'default': 'default',
        'choices': (
            ('default', _T('Default: full card display')),
            ('simple', _T('Simple: thumbnails with a minimal amount of meta data')),
            ('list', _T('List: thumbnails in their own row with useful meta data')),
            ('thumbnails', _T('Thumbnails: display only thumbnails')),
        ),
        'help': _T(
            'Set the default Dashboard view. '
            'This setting will affect how you experience Maio.'
        ),
    },
    'default_dashboard_sort': {
        'name': _T('Default Dashboard Sort'),
        'maio_type': MaioMapTypeChoices.TEXT,
        'max_length': 50,
        'default': '-date_added',
        'choices': (
            ('name', _T('Name (ascending A-Z)')),
            ('-name', _T('Name (descending Z-A)')),
            ('extension', _T('Extension (ascending A-Z)')),
            ('-extension', _T('Extension (descending Z-A)')),
            ('date_added', _T('Date Added (ascending 0-9)')),
            ('-date_added', _T('Date Added (descending 9-0)')),
            ('date_modified', _T('Date Modified (ascending 0-9)')),
            ('-date_modified', _T('Date Modified (descending 9-0)')),
            ('width', _T('Width (ascending 0-9)')),
            ('-width', _T('Width (descending 9-0)')),
            ('height', _T('Height (ascending 0-9)')),
            ('-height', _T('Height (descending 9-0)')),
            ('length', _T('Length (ascending 0-9)')),
            ('-length', _T('Length (descending 9-0)')),
            ('author', _T('Author (ascending A-Z)')),
            ('-author', _T('Author (descending Z-A)')),
            ('url', _T('URL (ascending A-Z)')),
            ('-url', _T('URL (descending Z-A)')),
            ('source', _T('Source (ascending A-Z)')),
            ('-source', _T('Source (descending Z-A)')),
            ('copyright', _T('Copyright (ascending A-Z)')),
            ('-copyright', _T('Copyright (descending Z-A)')),
        ),
        'help': _T(
            'Set the default Dashboard sorting method. '
            'This setting will affect how you experience Maio.'
        ),
    },
    'default_upload_media_view': {
        'name': _T('Default Upload Media View'),
        'maio_type': MaioMapTypeChoices.TEXT,
        'max_length': 50,
        'default': 'default',
        'choices': (
            ('default', _T('Default: full preview display')),
            ('simple', _T('Simple: thumbnails with a minimal amount of meta data')),
            ('list', _T('List: thumbnails in their own row with useful meta data')),
            ('thumbnails', _T('Thumbnails: display only thumbnails')),
        ),
        'help': _T(
            'Set the default Upload Media view. '
            'This setting will affect how you experience Maio.'
        ),
    },
    'auto_upload_media': {
        'name': _T('Auto Upload Media'),
        'maio_type': MaioMapTypeChoices.BOOL,
        'default': False,
        'help': _T(
            'Set whether or not to automatically upload media when choosing files.'
        ),
    },
    'redirect_to_previous_page_after_setting_save': {
        'name': _T('Redirect to Previous Page After Profile/Settings Save'),
        'maio_type': MaioMapTypeChoices.BOOL,
        'default': False,
        'help': _T(
            'Set whether or not to redirect to the previous page after saving '
            'this profile or these settings.'
        ),
    },
    'previous_page': {
        'name': _T('Previous Page'),
        'maio_type': MaioMapTypeChoices.URL,
        'max_length': 1024,
        'default': '/',
        'disabled': True,
        'help': _T('The page you came from.'),
    },
    'display_debug': {
        'name': _T('Display Debug'),
        'maio_type': MaioMapTypeChoices.BOOL,
        'default': False,
        'help': _T(
            'Display on-page and JavaScript debug information on each page? '
            'Regular users may ignore this setting as it only applies to Superusers.'
        ),
    },
}


class UserSettingMeta(ModelBase):
    '''Metaclass for Caption model.'''
    class Meta:
        verbose_name = 'User Setting'
        verbose_name_plural = 'User Settings'
        app_label = 'maio'
        db_table_comment = 'User system-wide settings.'
        get_latest_by = ['-date_modified']
        # order_with_respect_to = ['user', '-date_modified']
        ordering = ['-date_modified']
        # indexes = [
        #     Index(fields=('sort', 'name', 'is_default', 'date_added', '-date_modified'))
        # ]


class UserSetting(Model, metaclass=UserSettingMeta):
    '''UserSettings model.'''
    id = UUIDField(_T('UUID'), primary_key=True, default=uuid.uuid4, editable=False)
    user = ForeignKey(verbose_name=_T('Maio User'), to=MaioUser, on_delete=CASCADE)
    date_added = DateTimeField(_T('Date Added'), auto_now_add=True, editable=False)
    date_modified = DateTimeField(_T('Date Modified'), auto_now=True, editable=False)

    # Site-wide settings

    maio_theme = CharField(
        _T('Maio Theme'),
        max_length=USER_SETTINGS['maio_theme']['max_length'],
        default=USER_SETTINGS['maio_theme']['default'],
        choices=USER_SETTINGS['maio_theme']['choices'],
    )

    default_dashboard_view = CharField(
        _T('Default Dashboard View'),
        max_length=USER_SETTINGS['default_dashboard_view']['max_length'],
        default=USER_SETTINGS['default_dashboard_view']['default'],
        choices=USER_SETTINGS['default_dashboard_view']['choices'],
    )

    default_dashboard_sort = CharField(
        _T('Default Dashboard Sort'),
        max_length=USER_SETTINGS['default_dashboard_sort']['max_length'],
        default=USER_SETTINGS['default_dashboard_sort']['default'],
        choices=USER_SETTINGS['default_dashboard_sort']['choices'],
    )

    default_upload_media_view = CharField(
        _T('Default Upload Media View'),
        max_length=USER_SETTINGS['default_upload_media_view']['max_length'],
        default=USER_SETTINGS['default_upload_media_view']['default'],
        choices=USER_SETTINGS['default_upload_media_view']['choices'],
    )

    auto_upload_media = BooleanField(
        _T('Auto Upload Media'),
        default=USER_SETTINGS['auto_upload_media']['default'],
    )

    redirect_to_previous_page_after_setting_save = BooleanField(
        _T('Redirect to Previous Page After Settings Save'),
        default=USER_SETTINGS['redirect_to_previous_page_after_setting_save']['default'],
    )

    previous_page = CharField(
        _T('Previous Page'),
        default=USER_SETTINGS['previous_page']['default'],
        max_length=USER_SETTINGS['previous_page']['max_length'],
    )

    display_debug = BooleanField(
        _T('Display Debug'),
        default=USER_SETTINGS['display_debug']['default'],
    )

    # Non-model fields
    default_user_settings: dict[str, Any] = dict(USER_SETTINGS)

    def __str__(self) -> str:
        return f"[{str(self.id)[0:6]}] - ({self.user}) - {self.date_added}" # type: ignore
