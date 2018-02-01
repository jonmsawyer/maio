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

class File(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    mime_type = models.CharField(max_length=255)
    size = models.PositiveIntegerField(default=0)
    mtime = models.FloatField()
    md5sum = FixedCharField(max_length=32)
    tn_path = models.CharField(max_length=1024)
    file_path = models.CharField(max_length=1024)
    file_path_hash = FixedCharField(max_length=32, unique=True)
    rating = models.SmallIntegerField(null=True)
    views = models.PositiveIntegerField(default=0)
    media_length = models.PositiveIntegerField(null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['file_path']

    @staticmethod
    def get_all_images():
        Qr = None
        for key, value in mimetype_extension['image'].items():
            q = Q(**{"mime_type__exact": key})
            if Qr:
                Qr = Qr | q
            else:
                Qr = q
            
        files = File.objects.all().filter(Qr)
        return files

    def file_name(self):
        return self.file_path.split('/')[-1]
