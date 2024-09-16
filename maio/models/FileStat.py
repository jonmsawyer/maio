'''
File: Log.py

Module: ``maio.models.Log``
'''

from __future__ import annotations


from django.db.models import (
    Model, DateTimeField, PositiveBigIntegerField, BigAutoField,
)
from django.db.models.base import ModelBase
from django.utils.translation import gettext_lazy as _T

from maio.lib import sizeof_fmt


class FileStatMeta(ModelBase):
    '''Metaclass for Log model.'''
    name = 'File Stat'
    verbose_name = 'File Stats'
    app_label = 'maio'
    db_table_comment = 'Contains the number of files and their sizes of the current file store.'
    get_latest_by = ['-date_modified']
    # order_with_respect_to = ['user', 'date_added']
    ordering = ['-date_modified']


class FileStat(Model, metaclass=FileStatMeta):
    '''Log model.'''
    id = BigAutoField(_T('ID'), primary_key=True)
    num_images = PositiveBigIntegerField(_T('Number of Images'), editable=False)
    images_bytes = PositiveBigIntegerField(_T('Number of Bytes of Images'), editable=False)
    num_audio = PositiveBigIntegerField(_T('Number of Audio Files'), editable=False)
    audio_bytes = PositiveBigIntegerField(_T('Number of Bytes of Audio'), editable=False)
    num_videos = PositiveBigIntegerField(_T('Number of Videos'), editable=False)
    videos_bytes = PositiveBigIntegerField(_T('Number of Bytes of Video'), editable=False)
    num_documents = PositiveBigIntegerField(_T('Number of Documents'), editable=False)
    documents_bytes = PositiveBigIntegerField(_T('Number of Bytes of Documents'), editable=False)
    num_others = PositiveBigIntegerField(_T('Number of Other Files'), editable=False)
    others_bytes = PositiveBigIntegerField(_T('Number of Bytes of Other Files'), editable=False)
    date_added = DateTimeField(_T('Date Added'), auto_now_add=True)
    date_modified = DateTimeField(_T('Date Modified'), auto_now=True)

    def __str__(self) -> str:
        return (
            f"[{self.id}] - ({self.date_modified}) "
            f"Images: {self.num_images}; "
            f"Audio: {self.num_audio}; "
            f"Videos: {self.num_videos}; "
            f"Documents: {self.num_documents}; "
            f"Others: {self.num_others}"
        )

    def get_file_sizes_human(self) -> tuple[str, str, str, str, str]:
        '''Get the images size in human readable units.'''
        return (
            sizeof_fmt(self.images_bytes),
            sizeof_fmt(self.audio_bytes),
            sizeof_fmt(self.videos_bytes),
            sizeof_fmt(self.documents_bytes),
            sizeof_fmt(self.others_bytes),
        )

    @staticmethod
    def save_stats(
        num_images: int,
        images_bytes: int,
        num_audio: int,
        audio_bytes: int,
        num_videos: int,
        videos_bytes: int,
        num_documents: int,
        documents_bytes: int,
        num_others: int,
        others_bytes: int,
    ) -> FileStat:
        '''Save current File Stats.'''
        try:
            file_stat = FileStat.objects.get(
                num_images=num_images,
                images_bytes=images_bytes,
                num_audio=num_audio,
                audio_bytes=audio_bytes,
                num_videos=num_videos,
                videos_bytes=videos_bytes,
                num_documents=num_documents,
                documents_bytes=documents_bytes,
                num_others=num_others,
                others_bytes=others_bytes,
            )
        except FileStat.DoesNotExist:
            file_stat = FileStat(
                num_images=num_images,
                images_bytes=images_bytes,
                num_audio=num_audio,
                audio_bytes=audio_bytes,
                num_videos=num_videos,
                videos_bytes=videos_bytes,
                num_documents=num_documents,
                documents_bytes=documents_bytes,
                num_others=num_others,
                others_bytes=others_bytes,
            )
        file_stat.save()
        return file_stat
