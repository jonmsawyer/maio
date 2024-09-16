'''
File: __init__.py

Module: ``maio.views.ajax``

AJAX views for Maio.
'''

from __future__ import annotations

from .delete_media import delete_media


__all__: list[str] = [
    'delete_media',
]
