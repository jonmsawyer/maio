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

class Playlist(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(null=True)
    views = models.PositiveIntegerField(default=0)
    default_order = models.PositiveSmallIntegerField(default=0) # 0 random, 1 descending, 2 ascending
    time_between = models.PositiveIntegerField(default=5) # seconds
    media_class = models.PositiveSmallIntegerField(default=0) # 0 other, 1 image, 2 video, 3 audio, 4 text
