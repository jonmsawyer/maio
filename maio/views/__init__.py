'''
File: __init__.py

Module: ``maio.views``
'''

from .home import home
from .dashboard import dashboard
from .logout import logout
from .edit_profile import edit_profile
from .upload_media import UploadMediaView
from .search import search
from . import maio_admin

__all__: list[str] = [
    'home',
    'dashboard',
    'logout',
    'edit_profile',
    'UploadMediaView',
    'search',
    # Maio Admin
    'maio_admin',
]
