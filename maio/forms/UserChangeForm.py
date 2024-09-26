'''
File: UserChangeForm.py

Module: ``maio.forms.UserChangeForm``
'''

from __future__ import annotations
from typing import Any, Optional

from django.http import HttpRequest
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm as UCF
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _T


class UserChangeForm(UCF):
    '''The main profile form for Maio.'''
    request: Optional[HttpRequest] = None

    class Meta:
        model = User
        read_only_fields = ('date_joined')
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
        ]

    def __init__(self, *args: Any, **kwargs: Any):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    def clean_username(self) -> str:
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
            if self.request and self.request.user.id == user.id:
                return self.cleaned_data['username']
            raise ValidationError(
                _T("User `%(username)s` already exists. Please choose a different Username."),
                params={'username': self.cleaned_data['username']},
            )
        except User.DoesNotExist:
            pass

        return self.cleaned_data['username']
