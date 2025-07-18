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
    '''Converts a string into all lowercase'''
    return sizeof_duration_fmt(value)

@register.filter
def maio_filesize_human(value: int | float) -> str:
    '''Converts a string into all lowercase'''
    return sizeof_fmt(value)

@register.filter
def repeat(value: str, count: int) -> str:
    '''Repeats a string count times.'''
    return value*count

@register.filter
def mult(value: float, mult_by: float) -> float:
    '''Multiply a value by `mult_by`'''
    try:
        value = float(value)
    except ValueError:
        return value
    try:
        mult_by = float(mult_by)
    except ValueError:
        return value
    return value * mult_by

@register.filter
def hard_div(value: int, div_by: int) -> int:
    '''Hard divide two integers.'''
    try:
        value = int(value)
    except ValueError:
        return value
    try:
        div_by = int(div_by)
    except ValueError:
        return value
    return value // div_by
