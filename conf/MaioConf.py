'''
File: MaioConf.py

Module: ``conf.MaioConf``
'''

from __future__ import annotations
from typing import Any

import os


class MaioConf():
    '''Maio Configuration.'''
    def __init__(self, config: dict[str, Any] = {}) -> None:
        if config:
            self.config = config
        else:
            self.conf = {}

    def get_filestore_path(self) -> str:
        '''get_filestore_path'''
        return (
            self.config
                .get('filestore', {})
                .get('directory', '')
        )

    def get_media_path(self) -> str:
        '''get_media_path'''
        filestore_path = self.get_filestore_path()
        media_path = (
            self.config
                .get('media', {})
                .get('directory', '')
        )
        return os.path.join(filestore_path, media_path)

    def get_upload_path(self) -> str:
        '''get_upload_path'''
        filestore_path = self.get_filestore_path()
        upload_path = (
            self.config
                .get('upload', {})
                .get('directory', '')
        )
        return os.path.join(filestore_path, upload_path)

    def get_meta_path(self) -> str:
        '''get_meta_path'''
        filestore_path = self.get_filestore_path()
        meta_path = (
            self.config
                .get('meta', {})
                .get('directory', '')
        )
        return os.path.join(filestore_path, meta_path)

    def get_thumbnail_path(self) -> str:
        '''get_thumbnail_path'''
        media_path = self.get_media_path()
        thumbnail_path = (
            self.config
                .get('maio_types', {})
                .get('thumbnail', {})
                .get('directory', '')
        )
        return os.path.join(media_path, thumbnail_path)

    def get_images_path(self) -> str:
        '''get_images_path'''
        media_path = self.get_media_path()
        images_path = (
            self.config
                .get('maio_types', {})
                .get('image', {})
                .get('directory', '')
        )
        return os.path.join(media_path, images_path)

    def get_audio_path(self) -> str:
        '''get_audio_path'''
        media_path = self.get_media_path()
        audio_path = (
            self.config
                .get('maio_types', {})
                .get('audio', {})
                .get('directory', '')
        )
        return os.path.join(media_path, audio_path)

    def get_video_path(self) -> str:
        '''get_video_path'''
        media_path = self.get_media_path()
        video_path = (
            self.config
                .get('maio_types', {})
                .get('video', {})
                .get('directory', '')
        )
        return os.path.join(media_path, video_path)

    def get_document_path(self) -> str:
        '''get_document_path'''
        media_path = self.get_media_path()
        document_path = (
            self.config
                .get('maio_types', {})
                .get('document', {})
                .get('directory', '')
        )
        return os.path.join(media_path, document_path)

    def get_other_path(self) -> str:
        '''get_other_path'''
        media_path = self.get_media_path()
        other_path = (
            self.config
                .get('maio_types', {})
                .get('other', {})
                .get('directory', '')
        )
        return os.path.join(media_path, other_path)
