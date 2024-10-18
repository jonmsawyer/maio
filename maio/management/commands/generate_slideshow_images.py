'''
File: generate_slideshow_images.py

Module: ``maio.management.commands.generate_slideshow_images``

Generate slideshow images and thumbnails for Media (videos) that do not have any.
'''

from __future__ import annotations
from typing import Any, Dict

import os

# from django.core.management.base import CommandParser
from django.db.models import Q
from django.conf import settings

from conf import MaioConf

from maio import filestore as fs
from maio.models import MaioType, MaioTypeChoices, MaioMimeType, File

from ._base import MaioBaseCommand


maio_conf = MaioConf(config=settings.MAIO_SETTINGS)

class Command(MaioBaseCommand):
    help = 'Generate slideshow images for videos that do not have them.'

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
        slideshow_index = 0
        tn_static_root = maio_conf.get_chain('slideshow', 'static_uri')
        maio_type = MaioType.objects.filter(maio_type=MaioTypeChoices.VIDEO)
        video_type = MaioMimeType.objects.filter(maio_type__in=maio_type)
        files = File.objects.filter(Q(slideshow=None) | Q(thumbnail=None), mime_type__in=video_type)
        num_videos = 0
        num_media = 0
        for f in files:
            self.out(str(f))
            self.out(' > Generating slideshow... ', ending='')
            tn_path, is_created = f.process_thumbnail(update=True)
            self.out(f"{tn_path}; Created? {is_created}")
            num_videos += 1
            for m in f.media_set.all():
                md5_dir_slideshow = fs.mk_md5_dir_slideshow(f.md5sum)
                md5_1, md5_2 = (
                    md5_dir_slideshow.split('\\')[-2],
                    md5_dir_slideshow.split('\\')[-1],
                )
                slideshow_tn_uri = str(
                    os.path
                        .join(tn_static_root, md5_1, md5_2, f.get_tn_filename())
                        .replace('\\', '/')
                )
                slideshow_tn_uri = (
                    f"{slideshow_tn_uri.split('.')[0]}_{slideshow_index}"
                    f".{slideshow_tn_uri.split('.')[-1]}"
                )
                m.slideshow_index = slideshow_index
                m.slideshow_tn_uri = slideshow_tn_uri
                self.out(f' >>> Updating Media... {m}')
                m.save()
                num_media += 1
        self.out(f'Num videos updated: {num_videos}')
        self.out(f'Num media updated: {num_media}')
