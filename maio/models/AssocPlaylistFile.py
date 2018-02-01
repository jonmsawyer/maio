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

class AssocPlaylistFile(models.Model):
    playlist = models.ForeignKey(Playlist)
    file = models.ForeignKey(File)
    sort = models.PositiveIntegerField()