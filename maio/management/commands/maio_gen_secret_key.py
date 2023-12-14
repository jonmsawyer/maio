'''
File: maio_gen_secret_key.py

Module: ``maio.management.commands.maio_gen_secret_key``
'''

from __future__ import annotations
from typing import Any

from random import choice
from string import printable

from django.core.management.base import CommandParser

from ._base import MaioBaseCommand


NUM_CHARS: int = 66


class Command(MaioBaseCommand):
    args = '<None>'
    help = 'Generates a pseudorandom SECRET_KEY for use in `conf/site_settings.py`'

    def add_arguments(self, parser: CommandParser) -> None:
        # Positional arguments
        parser.add_argument(
            'num_chars', nargs='?', type=int, default=NUM_CHARS, metavar='NUM_CHARS',
            help=(
                'Generate a secret key with %(metavar)s characters. '
                'Default is %(default)s characters.'
            )
        )

    def handle(self, *args: Any, **options: dict[str, Any]) -> None:
        try:
            num_chars = int(options.get('num_chars', NUM_CHARS)) # type: ignore[reportGeneralTypeIssues]
        except (TypeError, ValueError):
            num_chars = NUM_CHARS
        secret_key = Command.gen_secret_key(num_chars)
        self.out(f"SECRET_KEY = '{secret_key.replace("'", "\\'")}'")

    @staticmethod
    def gen_secret_key(num_chars: int = NUM_CHARS) -> str:
        '''Generate a random secret key of length `num_chars`.'''
        return ''.join([choice(printable[:-6]) for _ in range(0, int(num_chars))])
