'''
File: LoginForm.py

Module: ``maio.forms.LoginForm``

Main log-in form for Maio.
'''

from __future__ import annotations
# from typing import Any

from django.forms import ModelForm #, CharField, TextInput, PasswordInput
# from django.utils.safestring import mark_safe

from maio.models import UserSetting


class UserSettingForm(ModelForm):
    '''The main user settings form for Maio.'''
    class Meta:
        model = UserSetting
        read_only_fields = ('date_added', 'date_modified')
        fields = [
            'default_dashboard_view',
            'default_dashboard_sort',
            'redirect_to_dashboard_after_setting_save',
        ]

    