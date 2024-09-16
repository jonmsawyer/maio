'''
File: lib.py

Module: ``maio.lib``

Maio Core library functions.
'''

from __future__ import annotations
from typing import Any, Optional

import re

from django.http import HttpRequest


def pre_populate_context_dict(
    request: HttpRequest,
    cd: Optional[dict[Any, Any]] = None,
) -> dict[Any, Any]:
    '''Pre-populate the context dictionary with common attributes.'''
    if cd is None:
        cd = {}
    cd = dict(cd)
    cd['file_stat'] = getattr(request, 'file_stat')
    cd['user_setting'] = getattr(request, 'user_setting')
    return cd


def sizeof_fmt(num: int | float, suffix: str = "B") -> str:
    '''
    Returns a size of bytes with a human readable suffix.

    Supports::

        * all currently known binary prefixes
        * negative and positive numbers
        * numbers larger than 1000 Yobibytes
        * arbitrary units (maybe you like to count in Gibibits!)

    Thanks to::

        https://stackoverflow.com/a/1094933
    '''
    for unit in ("", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"):
        if abs(num) < 1024.0:
            return f"{num:3.1f} {unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f} Yi{suffix}"


def validate_filename(filename: str) -> bool:
    '''
    Validate that the filename contains valid characters on Windows.

    According to: https://learn.microsoft.com/en-us/windows/win32/fileio/naming-a-file

    The following reserved characters are not allowed::

        * < (less than)
        * > (greater than)
        * : (colon)
        * " (double quote)
        * / (forward slash)
        * \\ (backslash)
        * | (vertical bar or pipe)
        * ? (question mark)
        * * (asterisk)
        * Integer value zero, sometimes referred to as the ASCII NUL character.
    '''
    invalid_chars_re = re.compile(r'[<>:"/\|?*\0]+')
    matches = invalid_chars_re.search(filename)
    if matches:
        return False
    return True
