'''
File: sync_maio_users.py

Module: ``maio.management.commands.sync_maio_users``

Purge the Media from the database and filesystem.

Doesn't work quite yet.
'''

from __future__ import annotations
from typing import Any, Dict

from django.core.management.base import BaseCommand

from maio.models import File, Media, Thumbnail, MetaFile

class Command(BaseCommand):
    help = 'Purge the Media from the database and filesystem.'

    def handle(self, *args: Any, **options: Dict[str, Any]) -> None:
        '''Purge all Media and File objects. Does not delete the files off the filesystem yet.'''
        print(f"Purged {Thumbnail.objects.all().delete()} Thumbnails.")
        print(f"Purged {MetaFile.objects.all().delete()} Meta files.")
        print(f"Purged {Media.objects.all().delete()} Media.")
        print(f"Purged {File.objects.all().delete()} Files.")
