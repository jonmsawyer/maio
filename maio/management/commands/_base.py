'''
File: _base.py

Module: ``maio.management.commands._base``
'''

from __future__ import annotations
from typing import Any

from pprint import pformat

from django.core.management.base import BaseCommand


class MaioBaseCommand(BaseCommand):
    args = '<None>'
    help = 'Extend MaioBaseCommand into a Command class to create a command for use in manage.py'
    can_import_settings = True

    def out(self, *args: Any, ending: str = '\n', flush: bool = True, **kwargs: Any) -> None:
        first_arg = True
        for arg in args:
            if first_arg:
                first_arg=False
            else:
                self.stdout.write(' ', ending='')
            if isinstance(arg, str):
                self.stdout.write(arg, ending='')
            else:
                self.stdout.write(pformat(arg), ending='')
        if kwargs:
            self.stdout.write(pformat(kwargs), ending='')
        self.stdout.write('', ending=ending)
        if flush:
            self.stdout.flush()
