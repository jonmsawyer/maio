import uuid

from django.db import models
from django.db.models import Q

from .maiofields import FixedCharField


mimetype_extension = {
    'image': {
        'image/gif': '.gif',
        'image/jpeg': '.jpg',
        'image/pjpeg': '.jpg',
        'image/png': '.png',
        'image/svg+xml': '.svg',
        'image/tiff': '.tiff',
        'image/bmp': '.bmp',
        'image/x-windows-bmp': '.bmp',
        'image/x-tiff': '.tiff',
    }
}

class Tag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255, unique=True)
    count = models.PositiveIntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    left_node = models.PositiveIntegerField(null=True, blank=True) # for v2
    right_node = models.PositiveIntegerField(null=True, blank=True) # for v2
