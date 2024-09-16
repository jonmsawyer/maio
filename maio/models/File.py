'''
File: File.py

Module: ``maio.models.File``
'''

from __future__ import annotations
# from typing import Any

import os
import uuid
import hashlib
import json
import subprocess

from django.db import IntegrityError

import magic # for mime types
from PIL import Image, ExifTags

from django.conf import settings
from django.utils import timezone
from django.http import HttpRequest
from django.core.files.uploadedfile import UploadedFile
from django.db.models import (
    Model, UUIDField, CharField, PositiveIntegerField, FloatField, DateTimeField, ForeignKey,
    FileField, Index, DO_NOTHING,
)
from django.db.models.base import ModelBase
from django.db import IntegrityError
from django.utils.datastructures import MultiValueDictKeyError
from django.utils.translation import gettext_lazy as _T

from conf import MaioConf
from maio import filestore as fs
from .MaioMimeType import MaioMimeType
from .MaioType import MaioType, MaioTypeChoices
from .Thumbnail import Thumbnail
from .MetaFile import MetaFile
from .Log import Log


maio_conf = MaioConf(config=settings.MAIO_SETTINGS)

class MimeTypeNotSetError(Exception):
    '''Raise this error when the `mime_type` field is not set.'''


class ContentFileNotSetError(Exception):
    '''Raise this error when the `content_file` field is not set.'''


class FileMeta(ModelBase):
    '''Metaclass for File model.'''
    name = 'File'
    verbose_name = 'Files'
    app_label = 'maio'
    db_table_comment = 'Files are saved to the hard drive, network, or cloud.'
    get_latest_by = ['-date_modified']
    # order_with_respect_to = ['']
    ordering = ['-date_modified']
    indexes = [
        Index(fields=(
            'original_name', 'size', 'mtime', '-modified_time', 'date_added', '-date_modified'
        ))
    ]


class File(Model, metaclass=FileMeta):
    '''File model. Represents a file stored in filestore/media.'''

    #: UUID unique ID.
    id = UUIDField(_T('UUID'), primary_key=True, default=uuid.uuid4, editable=False)

    #: The md5sum hash of the File, should be unique.
    md5sum = CharField(_T('MD5 Sum'), max_length=32, unique=True, editable=False)

    #: The base name for the File.
    original_name = CharField(_T('Original Name'), max_length=1024, editable=False)

    #: The File extension, if known.
    original_extension = CharField(_T('Original Extension'), max_length=8, editable=False, null=True, blank=True)

    #: The File's mime type.
    mime_type = ForeignKey(to=MaioMimeType, on_delete=DO_NOTHING, editable=False)

    #: The size, in bytes, of the File.
    size = PositiveIntegerField(_T('Size (Bytes)'), default=0, editable=False)

    #: File modified date, as a Unix time stamp.
    mtime = FloatField(_T('Unix Timestamp'), default=0.0, editable=False)

    #: File modified date, as a DateTime.
    modified_time = DateTimeField(_T('Modified Time'), auto_now_add=True)

    #: The File path stored in ./filestore/media/
    content_file = FileField(_T('Content File'), max_length=1024, upload_to=maio_conf.get_upload_path())

    #: The date time when this File was added to Maio.
    date_added = DateTimeField(_T('Date Added'), auto_now_add=True)

    #: The date time when this File was modified by Maio.
    date_modified = DateTimeField(_T('Date Modified'), auto_now=True)

    logger: Log | None = None

    def __str__(self) -> str:
        id = str(self.id)[0:6]
        return f"({id}) {self.get_filename()} - {self.mime_type} - {self.size} Bytes" # type: ignore

    # @staticmethod
    # def normalize_filename(filename: str) -> str:
    #     '''Remove multiple periods in file name.'''
    #     name = '.'.join(filename.split('.')[:-1])
    #     ext = filename.split('.')[-1]
    #     return f"{name}.{ext}"

    @staticmethod
    def handle_uploaded_file(
        request: HttpRequest,
        field: str,
    ) -> tuple[File, UploadedFile, bool]:
        '''Handle the uploaded file as given by `request.FILES`.'''
        logger = Log.new(request, 'File')
        try:
            content_file = request.FILES.get(field)
            maio_file = File(content_file=content_file)
        except MultiValueDictKeyError as e:
            logger.exception(str(e))
            raise e

        # maio_file.content_file.name = File.normalize_filename(maio_file.content_file.name)

        if content_file is None:
            e = ContentFileNotSetError('Content File is not set.')
            logger.exception(str(e))
            raise e

        # _deets = f'''
        #     Content File
        #     ------------
        #     Name: {maio_file.content_file.name}
        #     Size: {maio_file.content_file.size}
        #     Content Type: {content_file.content_type}
        #     Content Type Extra: {content_file.content_type_extra}
        #     Charset: {content_file.charset}
        #     Upload To: {maio_file.content_file.field.upload_to}
        #     Content Name: {content_file}
        #     Maio File Path: {maio_file.content_file.path}
        # '''
        # raise Exception(_deets)

        maio_file.calculate_md5sum()

        try:
            existing_file = File.objects.get(md5sum=maio_file.md5sum)
            is_created = False
            return existing_file, content_file, is_created
        except File.DoesNotExist:
            pass

        try:
            maio_file.save_upload_file()
            maio_file.calculate_mime_type()
            maio_file.set_filename()
            maio_file.process_media()
            maio_file.process_thumbnail()
            maio_file.set_data()
            maio_file.process_meta()
            is_created = True
            return maio_file, content_file, is_created
        except Exception as e:
            logger.exception(str(e))
            raise e

    def save_upload_file(self) -> None:
        '''Save the file referenced by `self.content_file`.'''
        path = os.path.join(File.content_file.field.upload_to, self.content_file.name)
        with open(path, 'wb+') as destination:
            for chunk in self.content_file.chunks():
                destination.write(chunk)

    def set_filename(self) -> str:
        '''Set the filename of this File.'''
        if not self.content_file:
            raise ContentFileNotSetError('`content_file` is not set.')
        self.original_name = '.'.join(self.content_file.name.split('.')[:-1])
        self.original_extension = ''.join(self.content_file.name.split('.')[-1])
        if not self.original_extension:
            ext = 'bin'
            try:
                extensions = MaioMimeType.objects.get(mime_type=self.mime_type).extensions
                extensions = extensions.split()
                if extensions:
                    ext = extensions[0]
            except MaioMimeType.DoesNotExist:
                raise
            self.original_extension = ext

    def set_data(self) -> bool:
        '''Set the data attributes of this object based on the uploaded file and input data.'''
        if not self.content_file:
            raise ContentFileNotSetError('`content_file` is not set.')
        now = timezone.now()
        self.size = self.content_file.size
        self.mtime = now.timestamp()
        self.modified_time = now
        try:
            maio_file = File.objects.get(md5sum=self.md5sum, mime_type=self.mime_type)
            created = False
        except File.DoesNotExist:
            self.save()
            created = True
        if not created:
            self = maio_file
        return created

    def calculate_md5sum(self) -> str:
        '''Return the md5sum of the file represented by this object.'''
        # path = os.path.join(File.content_file.field.upload_to, self.content_file.name)
        # self.md5sum = hashlib.md5(open(path, 'rb').read()).hexdigest()
        self.md5sum = hashlib.md5(self.content_file.read()).hexdigest()
        return self.md5sum

    def calculate_mime_type(self) -> MaioMimeType:
        '''Return the mime type of the file represented by this object.'''
        mime = magic.Magic(mime=True)
        path = os.path.join(File.content_file.field.upload_to, self.content_file.name)
        mimetype = str(mime.from_file(path))
        maio_mime_type, _created = MaioMimeType.objects.get_or_create(mime_type=mimetype)
        self.mime_type = maio_mime_type
        return self.mime_type

    def calculate_maio_type(self) -> MaioType:
        '''Return the MaioType of the file represented by this object.'''
        if not self.mime_type:
            raise MimeTypeNotSetError(
                '`mime_type` must be set in order to calculate the `MaioType`.'
            )
        return self.mime_type.maio_type

    def load_image(self) -> Image.Image:
        '''Load the image located at `self.content_file`.'''
        path = os.path.join(fs.mk_md5_dir_media(self.md5sum), self.get_filename())
        image = Image.open(path)
        image.load()
        return image.copy(), path

    def process_media(self) -> bool:
        '''Process the media for this file.'''
        path = os.path.join(File.content_file.field.upload_to, self.content_file.name)
        with open(path, 'rb') as fh:
            buf = fh.read()
        root = fs.mk_md5_dir_media(self.md5sum)
        if root:
            file_path = os.path.join(root, self.get_filename())
            with open(file_path, 'wb') as fh:
                fh.write(buf)
            os.unlink(path)
            self.content_file = file_path
            return True
        return False

    def process_thumbnail(self) -> bool | str:
        '''Process the thumbnail for this file.'''
        maio_type_choice = self.mime_type.maio_type.get_choice()
        root = fs.mk_md5_dir_thumbnail(self.md5sum)
        is_processed = False
        if maio_type_choice == MaioTypeChoices.IMAGE:
            tn_path = os.path.join(root, self.get_filename())
            try:
                # Thanks to: https://stackoverflow.com/a/6218425
                image, image_path = self.load_image()
                for orientation in ExifTags.TAGS.keys():
                    if ExifTags.TAGS[orientation] == 'Orientation':
                        break
                exif = dict(image.getexif().items())
                if orientation in exif:
                    if exif[orientation] == 3:
                        image=image.rotate(180, expand=True)
                    elif exif[orientation] == 6:
                        image=image.rotate(270, expand=True)
                    elif exif[orientation] == 8:
                        image=image.rotate(90, expand=True)
            except Exception:
                raise

            # _deets = f'''
            #     File Path: {file_path}
            #     Image Path: {image_path}
            # '''
            # raise Exception(_deets)

            image.thumbnail((300, 300), Image.Resampling.LANCZOS)
            image.save(tn_path)
            is_processed = True

        if maio_type_choice == MaioTypeChoices.VIDEO:
            tn_path = '.'.join(os.path.join(root, self.get_filename()).split('.')[:-1])
            tn_path = f"{tn_path}.jpg"
            ffmpeg_cmd: list[str] = [
                maio_conf.get_ffpmeg_bin_path(),
                "-ss", "00:00:01.00",
                "-i", os.path.join(fs.mk_md5_dir_media(self.md5sum), self.get_filename()),
                "-vf", "scale=300:300:force_original_aspect_ratio=decrease",
                "-vframes", "1",
                tn_path,
            ]
            # raise Exception(f"FFmpeg cmd: `{' '.join(ffmpeg_cmd)}`")
            try:
                _output = subprocess.run(ffmpeg_cmd, capture_output=True)
                image = Image.open(tn_path)
                image.load()
                is_processed = True
            except subprocess.CalledProcessError:
                raise

        if is_processed:
            try:
                self.thumbnail, _created = Thumbnail.objects.get_or_create(
                    file=self,
                    md5sum=self.md5sum,
                    content_file=tn_path,
                    width=image.width,
                    height=image.height,
                    size=os.stat(tn_path).st_size,
                )
            except IntegrityError:
                self.thumbnail = Thumbnail.objects.get(md5sum=self.md5sum)
            finally:
                image.close()
            return tn_path

        return False

    def process_meta(self) -> bool:
        '''Process the Metadata for this object.'''
        try:
            tn_path = Thumbnail.objects.get(md5sum=self.md5sum).content_file.path
        except Thumbnail.DoesNotExist:
            tn_path = '<None>'
        data = {
            'id': str(self.id),
            'md5sum': self.md5sum,
            'original_name': self.original_name,
            'original_extension': self.original_extension,
            'mime_type': self.mime_type.mime_type,
            'size': self.content_file.size,
            'mtime': os.stat(self.content_file.path).st_mtime,
            'modified_time': str(self.modified_time),
            'thumbnail': tn_path,
            'content_file': str(self.content_file.path),
            'date_added': str(self.date_added),
            'date_modified': str(self.date_modified),
        }
        data_str = json.dumps(data, indent=4) + os.linesep
        root = fs.mk_md5_dir_meta(self.md5sum)
        if root:
            file_path = os.path.join(root, self.get_filename()+'.json')
            with open(file_path, 'w', encoding='UTF-8') as fh:
                fh.write(data_str)
            try:
                self.meta_file, _created = MetaFile.objects.get_or_create(
                    file=self,
                    md5sum=self.md5sum,
                    content_file=file_path,
                )
            except IntegrityError:
                self.meta_file = MetaFile.objects.get(md5sum=self.md5sum)
            return True
        return False

    def get_filename(self) -> str:
        '''Generate the filename of this file.'''
        if self.original_extension:
            return f"{self.md5sum}.{self.original_extension}"
        return self.md5sum
