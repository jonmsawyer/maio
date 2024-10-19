'''
File: convert_audio.py

Module: ``maio.management.commands.convert_audio``

Convert all non-mp3 audio into `audio/mp3` format.
'''

from __future__ import annotations
from typing import Any, Dict

# import os

# from django.core.management.base import CommandParser
from django.db.models import Q
from django.conf import settings

from conf import MaioConf

# from maio import filestore as fs
from maio.models import MaioType, MaioTypeChoices, MaioMimeType, File

from ._base import MaioBaseCommand


maio_conf = MaioConf(config=settings.MAIO_SETTINGS)

class Command(MaioBaseCommand):
    help = 'Convert non-mp3 audio into audio/mpeg format for web listening.'

    # def add_arguments(self, parser: CommandParser) -> None:
    #     parser.add_argument(
    #        '-u', '--username', type=str, metavar='USERNAME', action='store', default=None,
    #        dest='username',
    #        help=(
    #             'Generate slideshow images for a given username. If this is not defined, -a or '
    #             '--all must be specified.'
    #         ),
    #     )
    #     parser.add_argument(
    #        '-a', '--all', action='store_true', default=False,
    #        dest='all',
    #        help=(
    #             'Generate slideshow images for all users. If this is not defined, -u or --username '
    #             'must be specified.'
    #         ),
    #     )

    def handle(self, *args: Any, **options: Dict[str, Any]) -> None:
        maio_type = MaioType.objects.filter(maio_type=MaioTypeChoices.AUDIO)
        audio_type = MaioMimeType.objects.filter(maio_type__in=maio_type)
        files = File.objects.filter(~Q(mime_type__mime_type='audio/mpeg'), mime_type__in=audio_type, is_converted=False)
        num_audio = 0
        for f in files:
            self.out(str(f))
            self.out(' > Converting audio...')
            converted, is_created = f.convert_audio()
            self.out(f' > {converted}; Created? {is_created}')
            f.is_converted = True
            f.save()
            num_audio += 1
        self.out(f'Num audio converted: {num_audio}')
