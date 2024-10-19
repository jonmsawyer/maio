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
        _T('%(value)s must be an integer between 1 and 1000, inclusive.'),
        params={'value': value}
    )
    if not isinstance(value, int):
        raise ve
    if value < 1 or value > 1000:
        raise ve
