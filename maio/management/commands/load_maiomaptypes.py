'''
File: load_maiomaptypes.py

Module: ``maio.management.commands.load_maiomaptypes``

Custom manage.py command. Loads the Maio Map Type data into the database.
'''

from __future__ import annotations
from typing import Any, Dict

from django.core.management.base import BaseCommand

from maio.models import MaioMapType

class Command(BaseCommand):
    help = 'Loads Maio Map Type data into the database.'

    #def add_arguments(self, parser):
    #    parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args: Any, **options: Dict[str, Any]) -> None:
        MaioMapType.default()
