'''
File: __init__.py

Package: ``maio.models``
'''

from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save


from .File import File
from .Caption import Caption
from .Media import Media
from .Playlist import Playlist
from .Tag import Tag
from .MaioMapType import MaioMapType, MaioMapTypeChoices
from .MaioMap import MaioMap
from .MaioUser import MaioUser
from .MaioType import MaioType, MaioTypeChoices
from .Love import Love
from .Like import Like
from .Rating import Rating


__all__: list[str] = [
    'File',
    'Caption',
    'Media',
    'Playlist',
    'Tag',
    'MaioMapType', 'MaioMapTypeChoices',
    'MaioMap',
    'MaioUser',
    'MaioType', 'MaioTypeChoices',
    'Love',
    'Like',
    'Rating',
]

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_maio_user(sender, instance=None, created=False, **kwargs) -> None: # type: ignore
    '''
    Hook into the `User` model's post-save signal and create a `MaioUser` associated with it.
    '''
    if created:
        MaioUser.objects.create(user=instance)
