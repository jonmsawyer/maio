'''
File: __init__.py

Package: ``maio.admin``
'''

from __future__ import annotations

from django.contrib.auth.models import User, Group, Permission

from maio.models import (
    File, Caption, Media, Playlist, Tag, MaioMap, MaioUser, MaioType, MaioMapType,
    Love, Like, Rating, MaioMimeType,
)

from .MaioAdminSite import MaioAdminSite
from .FileAdmin import FileAdmin
from .CaptionAdmin import CaptionAdmin
from .MediaAdmin import MediaAdmin
from .PlaylistAdmin import PlaylistAdmin
from .TagAdmin import TagAdmin
from .MaioMapAdmin import MaioMapAdmin
from .MaioUserAdmin import MaioUserAdmin
from .MaioTypeAdmin import MaioTypeAdmin
from .MaioMimeTypeAdmin import MaioMimeTypeAdmin
from .MaioMapTypeAdmin import MaioMapTypeAdmin
from .LoveAdmin import LoveAdmin
from .LikeAdmin import LikeAdmin
from .RatingAdmin import RatingAdmin
from .UserAdmin import UserAdmin
from .GroupAdmin import GroupAdmin
from .PermissionAdmin import PermissionAdmin


__all__: list[str] = [
    'MaioAdminSite',

    # Maio Admins
    'FileAdmin',
    'CaptionAdmin',
    'MediaAdmin',
    'PlaylistAdmin',
    'TagAdmin',
    'MaioMapAdmin',
    'MaioUserAdmin',
    'MaioTypeAdmin',
    'MaioMimeTypeAdmin',
    'MaioMapTypeAdmin',
    'LoveAdmin',
    'LikeAdmin',
    'RatingAdmin',

    # auth Admins
    'UserAdmin',
    'GroupAdmin',
    'PermissionAdmin',
]

admin_site = MaioAdminSite(name='admin')

# Maio Admins
admin_site.register(File, FileAdmin)
admin_site.register(Caption, CaptionAdmin)
admin_site.register(Media, MediaAdmin)
admin_site.register(Playlist, PlaylistAdmin)
admin_site.register(Tag, TagAdmin)
admin_site.register(MaioMap, MaioMapAdmin)
admin_site.register(MaioUser, MaioUserAdmin)
admin_site.register(MaioType, MaioTypeAdmin)
admin_site.register(MaioMimeType, MaioMimeTypeAdmin)
admin_site.register(MaioMapType, MaioMapTypeAdmin)
admin_site.register(Love, LoveAdmin)
admin_site.register(Like, LikeAdmin)
admin_site.register(Rating, RatingAdmin)

# auth Admins
admin_site.register(User, UserAdmin)
admin_site.register(Group, GroupAdmin)
admin_site.register(Permission, PermissionAdmin)
