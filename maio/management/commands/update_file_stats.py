'''
File: maio_get_images.py

Module: ``maio.management.commands.maio_get_images.py``
'''

from __future__ import annotations
from typing import Any

from maio.models import File, MaioType, MaioMimeType, FileStat
from maio.models.MaioType import MaioType, MaioTypeChoices

from ._base import MaioBaseCommand


class Command(MaioBaseCommand):
    '''
    This class is extended from :mod:`MaioBaseCommand` and is the driver for Maio's
    Django command to ingest images into Maio. Call this command with::
        $ manage.py update_file_stats

    For help, and to see other options, issue::
        $ manage.py update_file_stats --help
    '''
    help = 'Updates the file stats of the Maio ecosystem.'

    def handle(self, *args: Any, **options: Any) -> None:
        '''Handle this command.'''
        maio_type = MaioType.objects.filter(maio_type=MaioTypeChoices.IMAGE)
        image_type = MaioMimeType.objects.filter(maio_type__in=maio_type)
        images = File.objects.filter(mime_type__in=image_type)

        num_images = len(images)
        images_bytes = 0
        for image in images:
            images_bytes += int(image.size) # type: ignore

        print(f"Images: {num_images} totaling {images_bytes} bytes.")

        maio_type = MaioType.objects.filter(maio_type=MaioTypeChoices.AUDIO)
        audio_type = MaioMimeType.objects.filter(maio_type__in=maio_type)
        audio = File.objects.filter(mime_type__in=audio_type)

        num_audio = len(audio)
        audio_bytes = 0
        for aud in audio:
            audio_bytes += int(aud.size) # type: ignore

        print(f"Audio: {num_audio} totaling {audio_bytes} bytes.")

        maio_type = MaioType.objects.filter(maio_type=MaioTypeChoices.VIDEO)
        video_type = MaioMimeType.objects.filter(maio_type__in=maio_type)
        videos = File.objects.filter(mime_type__in=video_type)

        num_videos = len(videos)
        videos_bytes = 0
        for video in videos:
            videos_bytes += int(video.size) # type: ignore

        print(f"Videos: {num_videos} totaling {videos_bytes} bytes.")

        maio_type = MaioType.objects.filter(maio_type=MaioTypeChoices.DOCUMENT)
        document_type = MaioMimeType.objects.filter(maio_type__in=maio_type)
        documents = File.objects.filter(mime_type__in=document_type)

        num_documents = len(documents)
        documents_bytes = 0
        for document in documents:
            document_bytes += int(document.size) # type: ignore

        print(f"Documents: {num_documents} totaling {documents_bytes} bytes.")

        maio_type = MaioType.objects.filter(maio_type=MaioTypeChoices.OTHER)
        other_type = MaioMimeType.objects.filter(maio_type__in=maio_type)
        others = File.objects.filter(mime_type__in=other_type)

        num_others = len(others)
        others_bytes = 0
        for other in others:
            others_bytes += int(other.size) # type: ignore

        print(f"Others: {num_others} totaling {others_bytes} bytes.")

        FileStat.save_stats(
            num_images,
            images_bytes,
            num_audio,
            audio_bytes,
            num_videos,
            videos_bytes,
            num_documents,
            documents_bytes,
            num_others,
            others_bytes,
        )
