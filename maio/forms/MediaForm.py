'''
File: MediaForm.py

Module: ``maio.forms.MediaForm``
'''

from django.forms import ModelForm

from maio.models import Media


class MediaForm(ModelForm):
    '''Media form.'''
    class Meta:
        '''Metaclass for MediaForm.'''
        model = Media
        fields = [
            'file',
            'tags',
            'author',
            'url',
            'source',
            'copyright',
            'comment_type',
            'comment',
        ]
