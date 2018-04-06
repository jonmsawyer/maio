'''
File: File.py
Module: ``maio.models.File``
'''

# pylint:

import uuid

from django.db import models
from django.db.models import Q

from .maiofields import FixedCharField


#: Quick way of saying "NULL" for Django models
NULL = {'null': True, 'blank': True}


class File(models.Model):
    '''File object. Represents a file stored in filestore/media.'''
    
    #: UUID unique ID.
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    
    #: The md5sum hash of the File, should be unique.
    md5sum = FixedCharField(max_length=32, unique=True)
    
    #: The base name for the File.
    original_name = models.CharField(max_length=1024)
    
    #: The File extension, if known.
    original_extension = models.CharField(max_length=8, null=True, blank=True)
    
    #: The File's mime type.
    mime_type = models.CharField(max_length=64)
    
    #: The size, in bytes, of the File.
    size = models.PositiveIntegerField(default=0)
    
    #: File modified date, as a Unix time stamp.
    mtime = models.FloatField(default=0.0)
    
    #: The thumbnail path stored in ./filestore/thumbnails.
    tn_path = models.CharField(max_length=1024)
    
    #: The File path stored in ./filestore/media/images.
    file_path = models.CharField(max_length=1024)
    
    #: The date time when this File was added to Maio.
    date_added = models.DateTimeField(auto_now_add=True)
    
    #: The date time when this File was modified by Maio.
    date_modified = models.DateTimeField()
    
    class Meta:
        ordering = ['-date_modified']
    
    def __str__(self):
        return '({}) {}.{} - {} - {} bytes'.format(str(self.id)[0:6],
                                   self.original_name,
                                   self.original_extension,
                                   self.mime_type,
                                   self.size)
