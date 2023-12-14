'''
File: LoginForm.py

Module: ``maio.forms.LoginForm``

Main log-in form for Maio.
'''

from __future__ import annotations
from typing import Any

from django.forms import Form, CharField, TextInput, PasswordInput
from django.utils.safestring import mark_safe


class LoginForm(Form):
    '''The main log-in form for Maio.'''

    #: CharField form field for the username of the user.
    username = CharField(
        widget=TextInput(),
        max_length=50,
        required=True,
        label='Username'
    )

    #: CharField form field for the password of the user.
    password = CharField(
        widget=PasswordInput(render_value=True),
        max_length=50,
        required=True,
        label=mark_safe('Password')
    )

    # Method: clean
    # See: DocString
    def clean(self) -> dict[str, Any]:
        '''
        Main cleaning method.

        Validations::

            username - must not be empty string
            password - must not be empty string

        Raises:
        '''

        # Grab the entire dictionary of cleaned data. Subsequent values may be
        # NULL.
        data = super(LoginForm, self).clean()
        username = data.get('username')
        password = data.get('password')

        if not username or len(username) == 0:
            self.add_error('username', 'Empty username')
            data.pop('username', None)

        if not password or len(password) == 0:
            self.add_error('password', 'Empty password')
            data.pop('password', None)

        # Always return cleaned data. Return type is a dictionary.
        return data
