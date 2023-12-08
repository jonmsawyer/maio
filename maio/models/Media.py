import uuid
from collections import OrderedDict

from django.db import models
from django.db.models import Q

from django.contrib.auth.models import User

from maio import lib

from .File import File
from .Tag import Tag

from .maiofields import FixedCharField


#: Quick way of saying "NULL" for Django models
NULL = {'null': True, 'blank': True}

#: Choices for ``media_type`` field
MEDIA_TYPE_CHOICES = (
    ('image', 'Image'),
    ('video', 'Video'),
    ('audio', 'Audio'),
    ('document', 'Document'),
    ('other', 'Other'),
)


class Media(models.Model):
    '''
    Media class. Represents a sort of Meta class for a given File. Files may
    have many Media, but there's at least one Media per File is that File's
    ``media_class`` is ``image``.
    '''
    
    #: UUID unique ID.
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    
    #: The File that this Media points to.
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    
    #: The media's tags
    tags = models.ManyToManyField(Tag)
    
    #: One of ``['image', 'video', 'audio', 'document', 'other']``.
    media_type = models.CharField(max_length=8, choices=MEDIA_TYPE_CHOICES)
    
    #: Owner of the File
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    
    #: The base name for the File.
    name = models.CharField(max_length=1024)
    
    #: The File extension, if known.
    extension = models.CharField(max_length=8, **NULL)
    
    #: File modified date, as a Unix time stamp.
    mtime = models.FloatField(default=0.0)
    
    #: The File size.
    size = models.PositiveIntegerField(default=0)
    
    #: The date time when this File was added to Maio.
    date_added = models.DateTimeField(auto_now_add=True)
    
    #: The date time when this File was modified by Maio.
    date_modified = models.DateTimeField()
    
    #: The width in pixels of the Media
    width = models.PositiveIntegerField(**NULL)
    
    #: The height in pixes of the Media
    height = models.PositiveIntegerField(**NULL)
    
    #: The thumbnail width
    tn_width = models.PositiveIntegerField(**NULL)
    
    #: The thumbnail height
    tn_height = models.PositiveIntegerField(**NULL)
    
    #: The length (in milliseconds for Audio or Video, null for Image and Document)
    length = models.FloatField(**NULL)
    
    #: The number of loves that this Media has received. Loves is a higher
    #: order likes.
    is_loved = models.BooleanField(default=False)
    
    #: Whether or not this media is liked by the owner.
    is_liked = models.BooleanField(default=False)
    
    #: The rating given by the user.
    rating = models.PositiveSmallIntegerField(default=0)
    
    #: The author of this Media, if there is one.
    author = models.CharField(max_length=1024, **NULL)
    
    #: The URL source of this Media, if there is one.
    url = models.URLField(max_length=1024, **NULL)
    
    #: The text source of this Media, if there is one.
    source = models.CharField(max_length=1024, **NULL)
    
    #: The Copyright info of this Media, if there is one.
    copyright = models.CharField(max_length=128, **NULL)
    
    #: Some image formats store other meta data in the file, such as GPS location,
    #: lense information, type of camera, etc. What doesn't fit neatly into the
    #: fields above, goes into the ``comments`` field. Can be set to ``None``.
    comment = models.TextField(**NULL)
    
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
        ordering = ['-date_modified']
    
    def __str__(self):
        if self.extension:
            ext = '.'+self.extension
        return '({}) [{}] {}{} - {} bytes'.format(str(self.id)[:6],
                                                self.media_type,
                                                self.name,
                                                ext,
                                                self.size)
    
    @staticmethod
    def get_all_images(request):
        return Media.objects.filter(owner=request.user,
                                    media_type='image',
                                    is_active=True,
                                    is_hidden=False,
                                    is_deleted=False)
