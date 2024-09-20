'''
File: MaioConf.py

Module: ``conf.MaioConf``

Maio Configuration class for `settings.MAIO_SETTINGS`.
'''

from __future__ import annotations
from typing import Any, Optional


class MaioConf():
    '''Maio Configuration.'''
    def __init__(self, config: dict[str, Any] = {}) -> None:
        if config:
            self.config = config
        else:
            self.conf = {}

    @staticmethod
    def build_item_tree(*args: Any) -> dict[str, Any]:
        '''_build_item_tree'''
        tree: dict[str, Any] = {}
        place: dict[str, Any] = tree
        for arg in args:
            place[arg] = {}
            place = place[arg]
        return tree

    @staticmethod
    def find_item(obj: dict[str, Any], tree: dict[str, Any]) -> Optional[Any]:
        try:
            key, tree = tree.popitem()
        except KeyError:
            return obj

        if isinstance(obj, dict): # type: ignore
            if key in obj.keys() and tree:
                obj = obj[key]
            elif key in obj and not tree:
                return obj[key]

        if not isinstance(obj, dict): # type: ignore
            return None

        return MaioConf.find_item(obj, tree)

    def get_chain(self, *args: Any) -> Optional[Any]:
        '''
        Recursively retrieve the value identified by the chain of arguments. If no value can
        be found, then `NoneType` will be returned.
        '''
        tree = MaioConf.build_item_tree(*args)
        return MaioConf.find_item(dict(self.config), tree)

    # Images

    def get_images_path(self) -> Optional[str]:
        '''get_images_path'''
        # return self.get_chain('maio_types', 'image', 'media_directory')
        return self.get_chain('media', 'directory')

    def get_images_thumbnail_path(self) -> Optional[str]:
        '''get_images_path'''
        # return self.get_chain('maio_types', 'image', 'thumbnail_directory')
        return self.get_chain('maio_types', 'image', 'thumbnail_directory')

    # Audio

    def get_audio_path(self) -> Optional[str]:
        '''get_audio_path'''
        # return self.get_chain('maio_types', 'audio', 'media_directory')
        return self.get_chain('media', 'directory')

    def get_audio_thumbnail_path(self) -> Optional[str]:
        '''get_audio_thumbnail_path.'''
        return self.get_chain('maio_types', 'audio', 'thumbnail_path')

    # Video

    def get_video_path(self) -> Optional[str]:
        '''get_video_path'''
        # return self.get_chain('maio_types', 'video', 'media_directory')
        return self.get_chain('media', 'directory')

    # Slideshow

    def get_slideshow_directory(self) -> Optional[str]:
        '''get_slideshow_path'''
        # return self.get_chain('maio_types', 'slideshow', 'media_directory')
        return self.get_chain('slideshow', 'directory')

    def get_slideshow_static_uri(self) -> Optional[str]:
        '''get_slideshow_static_uri'''
        # return self.get_chain('maio_types', 'slideshow', 'media_directory')
        return self.get_chain('slideshow', 'static_uri')

    # Other

    def get_video_thumbnail_path(self) -> Optional[str]:
        '''get_video_thumbnail path.'''
        # return self.get_chain('maio_types', 'video', 'thumbnail_directory')
        return self.get_chain('thumbnail', 'directory')

    def get_other_path(self) -> Optional[str]:
        '''get_other_path'''
        # return self.get_chain('maio_types', 'other', 'media_directory')
        return self.get_chain('media', 'directory')

    # Static URIs

    def get_static_media_uri(self) -> Optional[str]:
        '''get_media_uri'''
        return self.get_chain('media', 'static_uri')

    def get_static_thumbnail_uri(self) -> Optional[str]:
        '''get_media_uri'''
        return self.get_chain('thumbnail', 'static_uri')

    # FFmpeg

    def get_ffpmeg_bin_path(self) -> Optional[str]:
        '''get_ffmpeg_bin_path'''
        return self.get_chain('ffmpeg', 'ffmpeg_exe')

    def get_ffprobe_bin_path(self) -> Optional[str]:
        '''get_ffplay_bin_path'''
        return self.get_chain('ffmpeg', 'ffprobe_exe')

    def get_ffplay_bin_path(self) -> Optional[str]:
        '''get_ffplay_bin_path'''
        return self.get_chain('ffmpeg', 'ffplay_exe')

    #
    # Document methods
    #

    def get_document_path(self) -> Optional[str]:
        '''get_document_path'''
        # return self.get_chain('maio_types', 'document', 'media_directory')
        return self.get_chain('media', 'directory')

    def get_document_thumbnail_path(self) -> Optional[str]:
        '''get_document_thumbnail_path'''
        return self.get_chain('maio_types', 'document', 'thumbnail_path')

    # PDF

    def get_document_pdf_extensions(self) -> Optional[list[str]]:
        '''get_document_pdf_extensions'''
        return self.get_chain('maio_types', 'document', 'pdf', 'extensions')

    def get_document_pdf_mime_types(self) -> Optional[list[str]]:
        '''get_document_pdf_mime_types'''
        return self.get_chain('maio_types', 'document', 'pdf', 'mime_types')

    def get_document_pdf_thumbnail_path(self) -> Optional[str]:
        '''get_document_pdf_mime_types'''
        return self.get_chain('maio_types', 'document', 'pdf', 'thumbnail_path')

    # MS Word / OpenDocument Word Processing Document

    def get_document_msword_extensions(self) -> Optional[list[str]]:
        '''get_document_msword_extensions'''
        return self.get_chain('maio_types', 'document', 'msword', 'extensions')

    def get_document_msword_mime_types(self) -> Optional[list[str]]:
        '''get_document_msword_mime_types'''
        return self.get_chain('maio_types', 'document', 'msword', 'mime_types')

    def get_document_msword_thumbnail_path(self) -> Optional[str]:
        '''get_document_msword_mime_types'''
        return self.get_chain('maio_types', 'document', 'msword', 'thumbnail_path')

    # MS Excel / OpenDocument Spreadsheet

    def get_document_msexcel_extensions(self) -> Optional[list[str]]:
        '''get_document_msexcel_extensions'''
        return self.get_chain('maio_types', 'document', 'msexcel', 'extensions')

    def get_document_msexcel_mime_types(self) -> Optional[list[str]]:
        '''get_document_msexcel_mime_types'''
        return self.get_chain('maio_types', 'document', 'msexcel', 'mime_types')

    def get_document_msexcel_thumbnail_path(self) -> Optional[str]:
        '''get_document_msexcel_mime_types'''
        return self.get_chain('maio_types', 'document', 'msexcel', 'thumbnail_path')

    # MS PowerPoint / OpenDocument Presentation

    def get_document_mspowerpoint_extensions(self) -> Optional[list[str]]:
        '''get_document_mspowerpoint_extensions'''
        return self.get_chain('maio_types', 'document', 'mspowerpoint', 'extensions')

    def get_document_mspowerpoint_mime_types(self) -> Optional[list[str]]:
        '''get_document_mspowerpoint_mime_types'''
        return self.get_chain('maio_types', 'document', 'mspowerpoint', 'mime_types')

    def get_document_msmspowerpoint_thumbnail_path(self) -> Optional[str]:
        '''get_document_msmspowerpoint_mime_types'''
        return self.get_chain('maio_types', 'document', 'mspowerpoint', 'thumbnail_path')

    # MS Access / OpenDocument Database

    def get_document_msaccess_extensions(self) -> Optional[list[str]]:
        '''get_document_msaccess_extensions'''
        return self.get_chain('maio_types', 'document', 'msaccess', 'extensions')

    def get_document_msaccess_mime_types(self) -> Optional[list[str]]:
        '''get_document_msaccess_mime_types'''
        return self.get_chain('maio_types', 'document', 'msaccess', 'mime_types')

    def get_document_msaccess_thumbnail_path(self) -> Optional[str]:
        '''get_document_msaccess_mime_types'''
        return self.get_chain('maio_types', 'document', 'msaccess', 'thumbnail_path')

    # XML

    def get_document_xml_extensions(self) -> Optional[list[str]]:
        '''get_document_xml_extensions'''
        return self.get_chain('maio_types', 'document', 'xml', 'extensions')

    def get_document_xml_mime_types(self) -> Optional[list[str]]:
        '''get_document_xml_mime_types'''
        return self.get_chain('maio_types', 'document', 'xml', 'mime_types')

    def get_document_xml_thumbnail_path(self) -> Optional[str]:
        '''get_document_xml_mime_types'''
        return self.get_chain('maio_types', 'document', 'xml', 'thumbnail_path')

    # Text

    def get_document_text_extensions(self) -> Optional[list[str]]:
        '''get_document_text_extensions'''
        return self.get_chain('maio_types', 'document', 'text', 'extensions')

    def get_document_text_mime_types(self) -> Optional[list[str]]:
        '''get_document_text_mime_types'''
        return self.get_chain('maio_types', 'document', 'text', 'mime_types')

    def get_document_text_thumbnail_path(self) -> Optional[str]:
        '''get_document_text_mime_types'''
        return self.get_chain('maio_types', 'document', 'text', 'thumbnail_path')
