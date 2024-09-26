'''
File: __init__.py

Package: ``maio.admin``
'''

from __future__ import annotations

from django.contrib.auth.models import User, Group, Permission

from maio.models import (
    File, Caption, Media, Playlist, Tag, MaioMap, MaioUser, MaioType, MaioMapType,
    Love, Like, Rating, MaioMimeType, FileStat, Log, MetaFile, Thumbnail, UserSetting,
    Slideshow, LibraryShare,
)

from .MaioAdminSite import MaioAdminSite

# Maio Admins
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
from .FileStatAdmin import FileStatAdmin
from .LogAdmin import LogAdmin
from .MetaFileAdmin import MetaFileAdmin
from .ThumbnailAdmin import ThumbnailAdmin
from .UserSettingAdmin import UserSettingAdmin
from .SlideshowAdmin import SlideshowAdmin
from .LibraryShareAdmin import LibraryShareAdmin

# auth Admins
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
    'FileStatAdmin',
    'LogAdmin',
    'MetaFileAdmin',
    'ThumbnailAdmin',
    'UserSettingAdmin',
    'SlideshowAdmin',
    'LibraryShareAdmin',

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
admin_site.register(FileStat, FileStatAdmin)
admin_site.register(Log, LogAdmin)
admin_site.register(MetaFile, MetaFileAdmin)
admin_site.register(Thumbnail, ThumbnailAdmin)
admin_site.register(UserSetting, UserSettingAdmin)
admin_site.register(Slideshow, SlideshowAdmin)
admin_site.register(LibraryShare, LibraryShareAdmin)

# auth Admins
admin_site.register(User, UserAdmin)
admin_site.register(Group, GroupAdmin)
admin_site.register(Permission, PermissionAdmin)
