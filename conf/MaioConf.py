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
        filestore_path = self.get_filestore_path()
        thumbnail_path = (
            self.config
                .get('thumbnail', {})
                .get('directory', '')
        )
        return os.path.join(filestore_path, thumbnail_path)

    def get_images_path(self) -> str:
        '''get_images_path'''
        filestore_path = self.get_filestore_path()
        images_path = (
            self.config
                .get('maio_types', {})
                .get('image', {})
                .get('directory', '')
        )
        return os.path.join(filestore_path, images_path)

    def get_audio_path(self) -> str:
        '''get_audio_path'''
        filestore_path = self.get_filestore_path()
        audio_path = (
            self.config
                .get('maio_types', {})
                .get('audio', {})
                .get('directory', '')
        )
        return os.path.join(filestore_path, audio_path)

    def get_audio_thumbnail_path(self) -> str:
        '''get_audio_thumbnail path.'''
        return (
            self.config
                .get('maio_types', {})
                .get('audio', {})
                .get('thumbnail_path', '')
        )

    def get_video_path(self) -> str:
        '''get_video_path'''
        filestore_path = self.get_filestore_path()
        video_path = (
            self.config
                .get('video', {})
                .get('directory', '')
        )
        return os.path.join(filestore_path, video_path)

    def get_document_path(self) -> str:
        '''get_document_path'''
        filestore_path = self.get_filestore_path()
        document_path = (
            self.config
                .get('document', {})
                .get('directory', '')
        )
        return os.path.join(filestore_path, document_path)

    def get_other_path(self) -> str:
        '''get_other_path'''
        filestore_path = self.get_filestore_path()
        other_path = (
            self.config
                .get('other', {})
                .get('directory', '')
        )
        return os.path.join(filestore_path, other_path)

    def get_static_media_uri(self) -> str | None:
        '''get_media_uri'''
        return self.config.get('media', {}).get('static_uri')

    def get_static_thumbnail_uri(self) -> str | None:
        '''get_media_uri'''
        return self.config.get('thumbnail', {}).get('static_uri')

    def get_ffpmeg_bin_path(self) -> str  | None:
        '''get_ffmpeg_bin_path'''
        return self.config.get('ffmpeg', {}).get('ffmpeg_exe')

    def get_ffprobe_bin_path(self) -> str  | None:
        '''get_ffplay_bin_path'''
        return self.config.get('ffmpeg', {}).get('ffprobe_exe')

    def get_ffplay_bin_path(self) -> str  | None:
        '''get_ffplay_bin_path'''
        return self.config.get('ffmpeg', {}).get('ffplay_exe')
