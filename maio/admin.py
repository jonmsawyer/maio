from django.contrib import admin
from django.contrib.admin import AdminSite

from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission

from maio.models import File
from maio.models import FileCaption
from maio.models import ImageFile
from maio.models import Playlist
from maio.models import PlaylistFileAssoc
from maio.models import Tag

class MaioAdminSite(AdminSite):
    site_header = 'Maio Administration'
    site_title = 'Maio Administration'

admin_site = MaioAdminSite(name='admin')

admin_site.register(File)
class FileAdmin(admin.ModelAdmin):
    pass

admin_site.register(FileCaption)
class FileCaptionAdmin(admin.ModelAdmin):
    pass

admin_site.register(ImageFile)
class ImageFileAdmin(admin.ModelAdmin):
    pass

admin_site.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    pass

admin_site.register(PlaylistFileAssoc)
class PlaylistFileAssocAdmin(admin.ModelAdmin):
    pass

admin_site.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass

admin_site.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

admin_site.register(Group)
class GroupAdmin(admin.ModelAdmin):
    pass

admin_site.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    pass
