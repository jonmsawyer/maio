'''
File: dump_mimetype_data.py

Module: ``maio.management.commands.dump_mimetype_data``

Dumps the MIME type data from the database into `./data/mime.types`.
'''

from __future__ import annotations
from typing import Any, Dict

from maio.models import MaioMimeType

from ._base import MaioBaseCommand


class Command(MaioBaseCommand):
    help = 'Dumps MIME type data from the database into `./data/mime.types`.'

    #def add_arguments(self, parser):
    #    parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args: Any, **options: Dict[str, Any]) -> None:
        MaioMimeType.dump_mimetype_data()

