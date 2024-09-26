'''
File: maio_extras.py

Module: ``maio.templatetags.maio_extras``

Extra template tags and filters.
'''

from __future__ import annotations

from django import template

from maio.lib import sizeof_duration_fmt, sizeof_fmt


register = template.Library()

@register.filter
def maio_duration_human(value: float) -> str:
    """Converts a string into all lowercase"""
    return sizeof_duration_fmt(value)

@register.filter
def maio_filesize_human(value: int | float) -> str:
    """Converts a string into all lowercase"""
    return sizeof_fmt(value)
