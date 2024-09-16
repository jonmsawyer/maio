'''
File: sync_maio_users.py

Module: ``maio.management.commands.sync_maio_users``

Custom manage.py command. Pruge the Media from the database and filesystem.
'''

from __future__ import annotations
from typing import Any, Dict

from django.core.management.base import BaseCommand
# from django.contrib.auth.models import User

from maio.models import File, Media, Thumbnail, MetaFile

class Command(BaseCommand):
    help = 'Pruge the Media from the database and filesystem.'

    #def add_arguments(self, parser):
    #    parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args: Any, **options: Dict[str, Any]) -> None:
        '''Purge all Media and File objects. Does not delete the files off the filesystem yet.'''
        print(f"Purged {Thumbnail.objects.all().delete()} Thumbnails.")
        print(f"Purged {MetaFile.objects.all().delete()} Meta files.")
        print(f"Purged {Media.objects.all().delete()} Media.")
        print(f"Purged {File.objects.all().delete()} Files.")
