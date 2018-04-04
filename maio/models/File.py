'''
File: File.py
Module: ``maio.models.File``
'''

# pylint:

import uuid

from django.db import models
from django.db.models import Q

from .maiofields import FixedCharField


MEDIA_CLASS_CHOICES = (
    ('images', 'Images'),
    ('video', 'Video'),
    ('audio', 'Audio'),
    ('documents', 'Documents'),
    ('other', 'Other'),
)

class File(models.Model):
    '''File object. Represents a file stored in filestore/media/images.'''
    
    #: UUID unique ID.
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    
    #: One of ``['images', 'video', 'audio', 'documents', 'other']``.
    media_class = models.CharField(max_length=32, choices=MEDIA_CLASS_CHOICES)
    
    #: The base name for the File.
    name = models.CharField(max_length=1024)
    
    #: The File extension, if known.
    extension = models.CharField(max_length=32, null=True, blank=True)
    
    #: The File's mime type.
    mime_type = models.CharField(max_length=64)
    
    #: The size, in bytes, of the File.
    num_bytes = models.PositiveIntegerField(default=0)
    
    #: File modified date, as a Unix time stamp.
    mtime = models.FloatField()
    
    #: The md5sum hash of the File, should be unique.
    md5sum = FixedCharField(max_length=32, unique=True)
    
    #: The thumbnail path stored in ./filestore/thumbnails.
    tn_path = models.CharField(max_length=1024)
    
    #: The File path stored in ./filestore/media/images.
    file_path = models.CharField(max_length=1024)
    
    #: The date time when this File was added to Maio.
    date_added = models.DateTimeField(auto_now_add=True)
    
    #: The date time when this File was modified by Maio.
    date_modified = models.DateTimeField(auto_now=True)
    
    #: Set to ``True`` to mark this File "active". An active File means that the File is
    #: searchable and is a valid file to include in Playlists, etc. A non-active File is
    #: hidden from the regular views and filters.
    #:
    #: Default: ``True``
    is_active = models.BooleanField(default=True)
    
    #: Set to ``True`` to mark this File as hidden. Only the owner of the File can see the
    #: File. Set to ``False`` to show this file in default views and filters.
    #:
    #: Default: ``False``
    is_hidden = models.BooleanField(default=False)
    
    #: Set to ``True`` if this File shall be marked for deletion. Akin to the Recycle Bin
    #: in Windows. Set to ``False`` to prevent this File from getting deleted. 
    #:
    #: Default: ``False``
    is_deleted = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-mtime']
