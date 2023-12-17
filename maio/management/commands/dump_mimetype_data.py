'''
File: dump_mimetype_data.py

Module: ``maio.management.commands.dump_mimetype_data``

Custom manage.py command. Dumps the MIME type data from the database into `./data/mime.types`.
'''

from __future__ import annotations
from typing import Any, Dict

from django.core.management.base import BaseCommand

from maio.models import MaioMimeType

class Command(BaseCommand):
    help = 'Dumps MIME type data from the database into `./data/mime.types`.'

    #def add_arguments(self, parser):
    #    parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args: Any, **options: Dict[str, Any]) -> None:
        MaioMimeType.dump_mimetype_data()
