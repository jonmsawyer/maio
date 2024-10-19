'''
File: __init__.py

Package: ``maio.filestore``

Maio's Filestore library.
'''

from __future__ import annotations

import os

from django.conf import settings

from conf import MaioConf


maio_conf = MaioConf(config=settings.MAIO_SETTINGS)


def mk_md5_dir(md5: str, root: str | None = None, length: int = 2) -> str:
    '''
    Make MD5 directory. Makes 3 directories under `root`, where the first 2 characters
    in `md5` make up the first directory, the next 2 characters make up the second
    directory, and the next 2 characters make up the third directory, each of them nested.

    If `root` is None, obtain the filestore root from MaioConf.

    # Raises

    * ValueError when the `md5` string is too short.
    * Any error from `os`.

    # Returns

    * str - The path to final directory structure.
    * None - When the directory to make was not made.
    '''
    if not root:
        root = maio_conf.get_filestore_path()
    if len(md5) >= length * 2:
        part1 = md5[0:length]
        part2 = md5[length:length * 2]
        dirtomake = os.path.join(root, part1, part2)
        os.makedirs(dirtomake, exist_ok=True)
        if os.path.isdir(dirtomake):
            return dirtomake
    raise ValueError('`md5` string is too short.')

def mk_md5_dir_media(md5: str, length: int = 2) -> str:
    '''Make MD5 directory under Media.'''
    return mk_md5_dir(md5, maio_conf.get_chain('media', 'directory'), length)

def mk_md5_dir_upload(md5: str, length: int = 2) -> str:
    '''Make MD5 directory under Upload.'''
    return mk_md5_dir(md5, maio_conf.get_chain('upload', 'directory'), length)

def mk_md5_dir_meta(md5: str, length: int = 2) -> str:
    '''Make MD5 directory under Meta.'''
    return mk_md5_dir(md5, maio_conf.get_chain('meta', 'directory'), length)

def mk_md5_dir_thumbnail(md5: str, length: int = 2) -> str:
    '''Make MD5 directory under Thumbnail.'''
    return mk_md5_dir(md5, maio_conf.get_chain('thumbnail', 'directory'), length)

def mk_md5_dir_slideshow(md5: str, length: int = 2) -> str:
    '''Make MD5 directory under Slideshow.'''
    return mk_md5_dir(md5, maio_conf.get_chain('slideshow', 'directory'), length)

def mk_md5_dir_converted(md5: str, length: int = 2) -> str:
    '''Make MD5 directory under Slideshow.'''
    return mk_md5_dir(md5, maio_conf.get_chain('converted', 'directory'), length)

def mk_md5_dir_images(md5: str, length: int = 2) -> str:
    '''Make MD5 directory under Images.'''
    return mk_md5_dir(md5, maio_conf.get_images_path(), length)

def mk_md5_dir_audio(md5: str, length: int = 2) -> str:
    '''Make MD5 directory under Audio.'''
    return mk_md5_dir(md5, maio_conf.get_audio_path(), length)

def mk_md5_dir_video(md5: str, length: int = 2) -> str:
    '''Make MD5 directory under Video.'''
    return mk_md5_dir(md5, maio_conf.get_video_path(), length)

def mk_md5_dir_document(md5: str, length: int = 2) -> str:
    '''Make MD5 directory under Document.'''
    return mk_md5_dir(md5, maio_conf.get_document_path(), length)

def mk_md5_dir_other(md5: str, length: int = 2) -> str:
    '''Make MD5 directory under Other.'''
    return mk_md5_dir(md5, maio_conf.get_other_path(), length)
