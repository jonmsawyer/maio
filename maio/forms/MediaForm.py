'''
File: MediaForm.py

Module: ``maio.forms.MediaForm``

Media form for Maio.
'''

from django.forms import ModelForm
# from django.forms.models import ModelFormMetaclass

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
