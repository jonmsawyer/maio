import uuid

from django.db import models
from django.db.models import Q

from .Media import Media
from .maiofields import FixedCharField


#: Quick way of saying "NULL" for Django models
NULL = {'null': True, 'blank': True}


class Caption(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    author = models.CharField(max_length=1024)
    url = models.URLField(max_length=1024, **NULL)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    caption_date = models.DateTimeField(null=True, blank=True)
    caption = models.TextField()
    
    class Meta:
        ordering = ['caption_date']
    
    def __str__(self):
        return '{} - {} - {}'.format(self.media.name, self.caption_date, self.caption[0:20])
