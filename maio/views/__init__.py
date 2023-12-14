'''
File: __init__.py

Module: ``maio.views``
'''

from .home import home
from .dashboard import dashboard
from .logout import logout
from .edit_profile import edit_profile
from .upload_media import upload_media
from .search import search


__all__: list[str] = [
    'home',
    'dashboard',
    'logout',
    'edit_profile',
    'upload_media',
    'search',
]
