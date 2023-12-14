'''
File: maiofields.py

Module: ``maio.models.maiofields``
'''

from __future__ import annotations
from typing import Any, Optional

from django.db.models import Field


class FixedCharField(Field): # type: ignore
    '''FixedCharField field.'''
    def __init__(self, verbose_name: str, max_length: int, *args: Any, **kwargs: Any) -> None:
        self.max_length = max_length
        super(FixedCharField, self).__init__(
            verbose_name=verbose_name,
            max_length=max_length,
            *args,
            **kwargs,
        )

    def db_type(self, connection: Optional[Any]) -> str:
        '''Return a string representing this database type.'''
        return f"char({self.max_length})"
