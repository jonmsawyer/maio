'''
File: load_mimetype_data.py

Module: ``maio.management.commands.load_mimetype_data``

Loads the MIME type data from `./data/mime.types` into the database.
'''

from __future__ import annotations
from typing import Any, Dict

from django.core.management.base import BaseCommand

from maio.models import MaioMimeType

class Command(BaseCommand):
    help = 'Loads MIME type data from `./data/mime.types` into the database.'

    def handle(self, *args: Any, **options: Dict[str, Any]) -> None:
        MaioMimeType.load_mimetype_data()
