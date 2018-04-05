from django.contrib import admin
from django.contrib.admin import AdminSite

from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission

from maio.models import File
from maio.models import Caption
from maio.models import Media
from maio.models import Playlist
from maio.models import Tag

class MaioAdminSite(AdminSite):
    site_header = 'Maio Administration'
    site_title = 'Maio Administration'

admin_site = MaioAdminSite(name='admin')

admin_site.register(File)
class FileAdmin(admin.ModelAdmin):
    pass

admin_site.register(Caption)
class CaptionAdmin(admin.ModelAdmin):
    pass

admin_site.register(Media)
class MediaAdmin(admin.ModelAdmin):
    pass

admin_site.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
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
