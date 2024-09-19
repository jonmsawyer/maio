'''
File: __init__.py

Package: ``maioadmin.views``

Views for Maio Admin.
'''

from __future__ import annotations

from .home import home
from .user_dashboard import user_dashboard


__all__: list[str] = [
    'home',
    'user_dashboard',
]
