'''
File: UserSettingForm.py

Module: ``maio.forms.UserSettingForm``
'''

from __future__ import annotations
from typing import Any

from django.forms import ModelForm, SelectDateWidget, TextInput

from maio.models import UserSetting
from maio.models.UserSetting import USER_SETTINGS as US


class UserSettingForm(ModelForm):
    '''The main user settings form for Maio.'''
    class Meta:
        model = UserSetting
        fields = [
            'maio_theme',
            'default_dashboard_view',
            'default_dashboard_sort',
            'default_dashboard_per_page',
            'default_upload_media_view',
            'auto_upload_media',
            'redirect_to_previous_page_after_setting_save',
            'display_debug',
        ]

        labels = {
            'maio_theme': US['maio_theme']['name'],
            'default_dashboard_view': US['default_dashboard_view']['name'],
            'default_dashboard_sort': US['default_dashboard_sort']['name'],
            'default_dashboard_per_page': US['default_dashboard_per_page']['name'],
            'default_upload_media_view': US['default_upload_media_view']['name'],
            'auto_upload_media': US['auto_upload_media']['name'],
            'redirect_to_previous_page_after_setting_save':
                US['redirect_to_previous_page_after_setting_save']['name'],
            'previous_page': US['previous_page']['name'],
            'display_debug': US['display_debug']['name'],
        }

        help_texts = {
            'maio_theme': US['maio_theme']['help'],
            'default_dashboard_view': US['default_dashboard_view']['help'],
            'default_dashboard_sort': US['default_dashboard_sort']['help'],
            'default_dashboard_per_page': US['default_dashboard_per_page']['help'],
            'default_upload_media_view': US['default_upload_media_view']['help'],
            'auto_upload_media': US['auto_upload_media']['help'],
            'redirect_to_previous_page_after_setting_save':
                US['redirect_to_previous_page_after_setting_save']['help'],
            'previous_page': US['previous_page']['help'],
            'display_debug': US['display_debug']['help'],
        }

        widgets: dict[str, Any] = {
            'date_added': SelectDateWidget(attrs={'disabled': True}),
            'date_modified': SelectDateWidget(attrs={'disabled': True}),
            'previous_page': TextInput(attrs={'disabled': True}),
        }
