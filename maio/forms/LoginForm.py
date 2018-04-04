'''File: JurorForm.py

Module: ``portal.forms.JurorForm``

Contains the JurorForm class used on the front page of the OQ portal.
'''

from datetime import datetime
import re

from django import forms
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    '''The main form as displayed on the ``portal:login`` screen. The user is asked
    for their last name, date of birth, jury summons ID, and the last four
    digits of their SSN.
    
    :init:
    
        .. code-block:: python
        
            form = LoginForm(request.POST or None)
    '''
    
    #: ``base_fields`` is an automatically generated attribute that is
    #: constructed based off of the form fields in this model.
    base_fields = None
    
    #: ``declared_fields`` is an automatically generated attribute that is
    #: constructed based off of the form fields in this model.
    declared_fields = None
    
    #: ``media`` is a meta class.
    media = None
    
    #: CharField form field for the username of the user.
    username = forms.CharField(widget=forms.TextInput(),
                               max_length=50,
                               required=True,
                               label='Username')
    
    #: CharField form field for the password of the user.
    password = forms.CharField(widget=forms.PasswordInput(render_value=True),
                               max_length=50,
                               required=True,
                               label=mark_safe('Password'))
    
    # Method: clean
    # See: DocString
    def clean(self):
        '''
        Main cleaning method. :func:`clean()` is performed after all
        :func:`clean_FIELD()` methods returned successfully.
        
        Validations:
        
            username - Value - must not be empty string
            password - Value - must not be empty string
        
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
