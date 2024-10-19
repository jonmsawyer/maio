'''
File: validators.py

Module: ``maio.validators``

Validators for Maio models.
'''

from __future__ import annotations

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _T


def validate_per_page(value: int) -> None:
    '''Validate per page.'''
    ve = ValidationError(
        _T('%(value)s must be an integer between 12 and 200, inclusive.'),
        params={'value': value}
    )
    if not isinstance(value, int):
        try:
            value = int(value)
        except TypeError:
            raise ve
    if value < 12 or value > 200:
        raise ve
