'''
File: FileForm.py

Module: ``maio.forms.FileForm``

Media form for Maio.
'''

from django.forms import ModelForm
# from django.forms.models import ModelFormMetaclass

from maio.models import File



class FileForm(ModelForm):
    '''Media form.'''
    class Meta:
        '''Metaclass for FileForm.'''
        model = File
        fields = [
            'content_file',
        ]
