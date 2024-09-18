'''
File: MaioConf.py

Module: ``conf.MaioConf``
'''

from __future__ import annotations
from typing import Any, Optional

import os


def _build_item_tree(*args: Any) -> dict[Any, Any]:
    '''_build_item_tree'''
    tree = {}
    place = tree
    for arg in args:
        place[arg] = {}
        place = place[arg]
    return tree

def _find_item(obj, key):
    if key in obj: return obj[key]
    for k, v in obj.items():
        if isinstance(v,dict):
            item = _finditem(v, key)
            if item is not None:
                return item


class MaioConf():
    '''Maio Configuration.'''
    def __init__(self, config: dict[str, Any] = {}) -> None:
        if config:
            self.config = config
        else:
            self.conf = {}

    def get_chain(self, *args: Any) -> Optional[Any]:
        '''
        Recursively retrieve the value identified by the chain of arguments. If no value can
        be found, then `NoneType` will be returned.
        '''
        tree = _build_item_tree(*args)
        item = _find_item(self.config)
        if args:
            if args[1] in self.config:
                pass

    def get_filestore_directory(self) -> str:
        '''get_filestore_directory'''
        return (
            self.config
                .get('filestore', {})
                .get('directory', '')
        )

    def get_media_directory(self) -> str:
        '''get_media_directory'''
        return (
            self.config
                .get('media', {})
                .get('directory', '')
        )

    def get_upload_directory(self) -> str:
        '''get_upload_directory'''
        return (
            self.config
                .get('upload', {})
                .get('directory', '')
        )

    def get_meta_directory(self) -> str:
        '''get_meta_directory'''
        return (
            self.config
                .get('meta', {})
                .get('directory', '')
        )

    def get_thumbnail_directory(self) -> str:
        '''get_thumbnail_directory'''
        return (
            self.config
                .get('thumbnail', {})
                .get('directory', '')
        )

    # Images

    def get_images_path(self) -> str:
        '''get_images_path'''
        filestore_path = self.get_filestore_path()
        images_path = (
            self.config
                .get('maio_types', {})
                .get('image', {})
                .get('media_directory', '')
        )
        return os.path.join(filestore_path, images_path)

    def get_images_thumbnail_path(self) -> str:
        '''get_images_path'''
        filestore_path = self.get_filestore_path()
        images_path = (
            self.config
                .get('maio_types', {})
                .get('image', {})
                .get('thumbnail_directory', '')
        )
        return os.path.join(filestore_path, images_path)

    # Audio

    def get_audio_path(self) -> str:
        '''get_audio_path'''
        filestore_path = self.get_filestore_path()
        audio_path = (
            self.config
                .get('maio_types', {})
                .get('audio', {})
                .get('media_directory', '')
        )
        return os.path.join(filestore_path, audio_path)

    def get_audio_thumbnail_path(self) -> str:
        '''get_audio_thumbnail_path.'''
        return (
            self.config
                .get('maio_types', {})
                .get('audio', {})
                .get('thumbnail_path', '')
        )

    # Video

    def get_video_path(self) -> str:
        '''get_video_path'''
        filestore_path = self.get_filestore_path()
        video_path = (
            self.config
                .get('maio_types', {})
                .get('video', {})
                .get('media_directory', '')
        )
        return os.path.join(filestore_path, video_path)

    def get_video_thumbnail_path(self) -> str:
        '''get_video_thumbnail path.'''
        return (
            self.config
                .get('maio_types', {})
                .get('video', {})
                .get('thumbnail_path', '')
        )

    def get_document_path(self) -> str:
        '''get_document_path'''
        filestore_path = self.get_filestore_path()
        document_path = (
            self.config
                .get('maio_types', {})
                .get('document', {})
                .get('media_directory', '')
        )
        return os.path.join(filestore_path, document_path)

    def get_other_path(self) -> str:
        '''get_other_path'''
        filestore_path = self.get_filestore_path()
        other_path = (
            self.config
                .get('maio_types', {})
                .get('other', {})
                .get('media_directory', '')
        )
        return os.path.join(filestore_path, other_path)

    def get_static_media_uri(self) -> str | None:
        '''get_media_uri'''
        return self.config.get('media', {}).get('static_uri')

    def get_static_thumbnail_uri(self) -> str | None:
        '''get_media_uri'''
        return self.config.get('thumbnail', {}).get('static_uri')

    def get_ffpmeg_bin_path(self) -> str | None:
        '''get_ffmpeg_bin_path'''
        return self.config.get('ffmpeg', {}).get('ffmpeg_exe')

    def get_ffprobe_bin_path(self) -> str | None:
        '''get_ffplay_bin_path'''
        return self.config.get('ffmpeg', {}).get('ffprobe_exe')

    def get_ffplay_bin_path(self) -> str | None:
        '''get_ffplay_bin_path'''
        return self.config.get('ffmpeg', {}).get('ffplay_exe')

    #
    # Document methods
    #

    def get_document_thumbnail_path(self) -> str | None:
        '''get_document_thumbnail_path'''
        return (
            self.config
                .get('maio_types', {})
                .get('document', {})
                .get('thumbnail_path')
        )

    # PDF

    def get_document_pdf_extensions(self) -> list[str] | None:
        '''get_document_pdf_extensions'''
        return (
            self.config
                .get('maio_types', {})
                .get('document', {})
                .get('pdf', {})
                .get('extensions')
        )

    def get_document_pdf_mime_types(self) -> list[str] | None:
        '''get_document_pdf_mime_types'''
        return (
            self.config
                .get('maio_types', {})
                .get('document', {})
                .get('pdf', {})
                .get('mime_types')
        )

    def get_document_pdf_thumbnail_path(self) -> str | None:
        '''get_document_pdf_mime_types'''
        return (
            self.config
                .get('maio_types', {})
                .get('document', {})
                .get('pdf', {})
                .get('thumbnail_path')
        )

    # MS Word / OpenDocument Word Processing Document

    def get_document_msword_extensions(self) -> list[str] | None:
        '''get_document_msword_extensions'''
        return (
            self.config
                .get('maio_types', {})
                .get('document', {})
                .get('msword', {})
                .get('extensions')
        )

    def get_document_msword_mime_types(self) -> list[str] | None:
        '''get_document_msword_mime_types'''
        return (
            self.config
                .get('maio_types', {})
                .get('document', {})
                .get('msword', {})
                .get('mime_types')
        )

    def get_document_msword_thumbnail_path(self) -> str | None:
        '''get_document_msword_mime_types'''
        return (
            self.config
                .get('maio_types', {})
                .get('document', {})
                .get('msword', {})
                .get('thumbnail_path')
        )

    # MS Excel / OpenDocument Spreadsheet

    def get_document_msexcel_extensions(self) -> list[str] | None:
        '''get_document_msexcel_extensions'''
        return (
            self.config
                .get('maio_types', {})
                .get('document', {})
                .get('msexcel', {})
                .get('extensions')
        )

    def get_document_msexcel_mime_types(self) -> list[str] | None:
        '''get_document_msexcel_mime_types'''
        return (
            self.config
                .get('maio_types', {})
                .get('document', {})
                .get('msexcel', {})
                .get('mime_types')
        )

    def get_document_msexcel_thumbnail_path(self) -> str | None:
        '''get_document_msexcel_mime_types'''
        return (
            self.config
                .get('maio_types', {})
                .get('document', {})
                .get('msexcel', {})
                .get('thumbnail_path')
        )

    # MS PowerPoint / OpenDocument Presentation

    def get_document_mspowerpoint_extensions(self) -> list[str] | None:
        '''get_document_mspowerpoint_extensions'''
        return (
            self.config
                .get('maio_types', {})
                .get('document', {})
                .get('mspowerpoint', {})
                .get('extensions')
        )

    def get_document_mspowerpoint_mime_types(self) -> list[str] | None:
        '''get_document_mspowerpoint_mime_types'''
        return (
            self.config
                .get('maio_types', {})
                .get('document', {})
                .get('mspowerpoint', {})
                .get('mime_types')
        )

    def get_document_msmspowerpoint_thumbnail_path(self) -> str | None:
        '''get_document_msmspowerpoint_mime_types'''
        return (
            self.config
                .get('maio_types', {})
                .get('document', {})
                .get('mspowerpoint', {})
                .get('thumbnail_path')
        )

    # MS Access / OpenDocument Database

    def get_document_msaccess_extensions(self) -> list[str] | None:
        '''get_document_msaccess_extensions'''
        return (
            self.config
                .get('maio_types', {})
                .get('document', {})
                .get('msaccess', {})
                .get('extensions')
        )

    def get_document_msaccess_mime_types(self) -> list[str] | None:
        '''get_document_msaccess_mime_types'''
        return (
            self.config
                .get('maio_types', {})
                .get('document', {})
                .get('msaccess', {})
                .get('mime_types')
        )

    def get_document_msaccess_thumbnail_path(self) -> str | None:
        '''get_document_msaccess_mime_types'''
        return (
            self.config
                .get('maio_types', {})
                .get('document', {})
                .get('msaccess', {})
                .get('thumbnail_path')
        )

    # XML

    def get_document_xml_extensions(self) -> list[str] | None:
        '''get_document_xml_extensions'''
        return (
            self.config
                .get('maio_types', {})
                .get('document', {})
                .get('xml', {})
                .get('extensions')
        )

    def get_document_xml_mime_types(self) -> list[str] | None:
        '''get_document_xml_mime_types'''
        return (
            self.config
                .get('maio_types', {})
                .get('document', {})
                .get('xml', {})
                .get('mime_types')
        )

    def get_document_xml_thumbnail_path(self) -> str | None:
        '''get_document_xml_mime_types'''
        return (
            self.config
                .get('maio_types', {})
                .get('document', {})
                .get('xml', {})
                .get('thumbnail_path')
        )

    # Text

    def get_document_text_extensions(self) -> list[str] | None:
        '''get_document_text_extensions'''
        return (
            self.config
                .get('maio_types', {})
                .get('document', {})
                .get('text', {})
                .get('extensions')
        )

    def get_document_text_mime_types(self) -> list[str] | None:
        '''get_document_text_mime_types'''
        return (
            self.config
                .get('maio_types', {})
                .get('document', {})
                .get('text', {})
                .get('mime_types')
        )

    def get_document_text_thumbnail_path(self) -> str | None:
        '''get_document_text_mime_types'''
        return (
            self.config
                .get('maio_types', {})
                .get('document', {})
                .get('text', {})
                .get('thumbnail_path')
        )
