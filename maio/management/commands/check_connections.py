'''
File: check_connections.py

Module: ``maio.management.commands.check_connections``

Custom manage.py command. Check the connection status of all database defined in
`settings.DATABASES`.
'''

from __future__ import annotations
from typing import Any, Dict

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import connections


class Command(BaseCommand):
    help = 'Checks all database connections as defined in `setting.DATABASES`.'

    #def add_arguments(self, parser):
    #    parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args: Any, **options: Dict[str, Any]) -> None:
        for key in settings.DATABASES.keys():
            self.stdout.write('{} ... '.format(key), ending='')
            try:
                db_conn = connections[key]
                with db_conn.cursor() as _cursor:
                    self.stdout.write('OK')
            except Exception as e:
                self.stdout.write('FAIL: {}'.format(e))
