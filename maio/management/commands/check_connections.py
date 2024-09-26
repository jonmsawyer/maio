'''
File: check_connections.py

Module: ``maio.management.commands.check_connections``

Check the connection status of all databases defined in `settings.DATABASES`.
'''

from __future__ import annotations
from typing import Any, Dict

from django.conf import settings
from django.db import connections


from ._base import MaioBaseCommand

class Command(MaioBaseCommand):
    help = 'Checks all database connections as defined in `setting.DATABASES`.'

    def handle(self, *args: Any, **options: Dict[str, Any]) -> None:
        for key in settings.DATABASES.keys():
            self.out('{} ... '.format(key), ending='')
            try:
                db_conn = connections[key]
                with db_conn.cursor() as _cursor:
                    self.out('OK')
            except Exception as e:
                self.out('FAIL: {}'.format(e))
