from django.db import models

from .ImageFile import ImageFile
from .Tag import Tag


class TagImageFileAssoc(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    image_file = models.ForeignKey(ImageFile, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['tag']
