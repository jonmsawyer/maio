'''
File:

Module: ``maio.models.choices``
'''

from __future__ import annotations
# from typing import Any

from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _T


__all__: list[str] = [
    'PermissionChoices',
]


class PermissionChoices(TextChoices):
    '''Text choices any model needing Permission.'''
    DENIED = 'denied', _T('Denied')
    CREATE = 'create', _T('Create')
    READ = 'read', _T('Read')
    UPDATE = 'update', _T('Update')
    DELETE = 'delete', _T('Delete')
