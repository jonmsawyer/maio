import uuid

from django.db import models
from django.db.models import Q

from .File import File
from .maiofields import FixedCharField


class FileCaption(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    author = models.CharField(max_length=1024)
    date_added = models.DateTimeField(auto_now_add=True)
    caption_date = models.DateTimeField(null=True, blank=True)
    caption = models.TextField()
    
    class Meta:
        ordering = ['date_added']
