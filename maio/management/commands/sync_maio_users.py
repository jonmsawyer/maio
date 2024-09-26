'''
File: sync_maio_users.py

Module: ``maio.management.commands.sync_maio_users``

Sync up Maio Users from the `auth` contrib Users table.
'''

from __future__ import annotations
from typing import Any, Dict

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from maio.models import MaioUser

class Command(BaseCommand):
    help = 'Sync up Maio Users from the `auth` contrib Users table.'

    def handle(self, *args: Any, **options: Dict[str, Any]) -> None:
        for user in User.objects.all():
            MaioUser.objects.get_or_create(user=user)
