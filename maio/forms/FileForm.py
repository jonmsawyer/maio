'''
File: FileForm.py

Module: ``maio.forms.FileForm``

Media form for Maio.
'''

from __future__ import annotations
from typing import Any, Optional

from django import forms
# from django.forms.models import ModelFormMetaclass
# from django.forms import FileField, ClearableFileInput

from maio.models import File

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args: Any, **kwargs: Any):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data: list[Any] | tuple[Any, ...], initial: Optional[Any] = None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class FileForm(forms.ModelForm):
    '''Media form.'''
    content_file = MultipleFileField(label='Select files...', required=False)
    skip_duplicates = forms.BooleanField(label='Skip duplicate media?', required=False, initial=True)

    class Meta:
        '''Metaclass for FileForm.'''
        model = File
        fields = [
            'content_file',
            'skip_duplicates',
        ]
