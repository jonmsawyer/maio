'''
File: sync_user_settings.py

Module: ``maio.management.commands.sync_user_settings``

Syncs the User Settings database table with current Maio Users.
'''

from __future__ import annotations
from typing import Any

from django.core.management.base import BaseCommand

from maio.models import MaioUser, UserSetting

class Command(BaseCommand):
    help = 'Syncs the User Settings database table with current Maio Users.'

    #def add_arguments(self, parser):
    #    parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args: Any, **options: dict[str, Any]) -> None:
        for user in MaioUser.objects.all():
            UserSetting.objects.get_or_create(user=user)
