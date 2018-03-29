import uuid
from collections import OrderedDict

from django.db import models
from django.db.models import Q

from maio import lib

from .File import File
from .maiofields import FixedCharField

#: Quick way of saying "NULL" for Django models
NULL = {'null': True, 'blank': True}

class ImageFile(models.Model):
    '''
    ImageFile class. Represents a sort of Meta class for a given File. Files may
    have many ImageFiles, but there's at least one ImageFile per File is that File's
    ``media_class`` is ``image``.
    '''
    
    #: UUID unique ID.
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    
    #: The File that this ImageFile points to.
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    
    #: The base name for the File.
    name = models.CharField(max_length=1024)
    
    #: The File extension, if known.
    extension = models.CharField(max_length=32, **NULL)
    
    #: File modified date, as a Unix time stamp.
    mtime = models.FloatField(default=0.0)
    
    #: The date time when this File was added to Maio.
    date_added = models.DateTimeField(auto_now_add=True)
    
    #: The date time when this File was modified by Maio.
    date_modified = models.DateTimeField(auto_now=True)
    
    #: The width in pixels of the ImageFile
    width = models.PositiveIntegerField(default=0)
    
    #: The height in pixes of the ImageFile
    height = models.PositiveIntegerField(default=0)
    
    #: The number of loves that this ImageFile has received. Loves is a higher
    #: order likes.
    loves = models.PositiveIntegerField(default=0)
    
    #: The number of likes that this ImageFile has received. Likes rate higher
    #: than dislikes, but do not rate as high as loves.
    likes = models.PositiveIntegerField(default=0)
    
    #: The number of dislikes that this ImageFile has received. Rates lower than
    #: both loves and likes.
    dislikes = models.PositiveIntegerField(default=0)
    
    #: The number of times this ImageFile has been viewed.
    views = models.PositiveIntegerField(default=0)
    
    #: The URL source of this ImageFile, if there is one.
    url = models.URLField(max_length=1024, **NULL)
    
    #: The author of this ImageFile, if there is one.
    author = models.CharField(max_length=1024, **NULL)
    
    #: The text source of this ImageFile, if there is one.
    source = models.CharField(max_length=1024, **NULL)
    
    #: The Copyright info of this ImageFile, if there is one.
    copyright = models.CharField(max_length=128, **NULL)
    
    #: Some image formats store other meta data in the file, such as GPS location,
    #: lense information, type of camera, etc. What doesn't fit neatly into the
    #: fields above, goes into the ``comments`` field. Can be set to ``None``.
    comments = models.TextField(**NULL)
    
    class Meta:
        ordering = ['-mtime']
    
    @staticmethod
    def get_all_images():
        #Qr = None
        #for key, value in lib.MIMETYPE_EXTENSION['image'].items():
        #    q = Q(**{"mime_type__exact": key})
        #    if Qr:
        #        Qr = Qr | q
        #    else:
        #        Qr = q
        #    
        #files = File.objects.filter(Qr)
        return File.objects.filter(media_class="image")
