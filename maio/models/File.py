'''
File: File.py

Module: ``maio.models.File``
'''

from __future__ import annotations
from typing import Any, Optional

import os
import uuid
import hashlib
import json
import subprocess
from unidecode import unidecode

import numpy
import ffmpeg
import magic # for mime types
from PIL import Image, ExifTags

from django.db import IntegrityError
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
from .Slideshow import Slideshow


maio_conf = MaioConf(config=settings.MAIO_SETTINGS)

class MimeTypeNotSetError(Exception):
    '''Raise this error when the `mime_type` field is not set.'''


class ContentFileNotSetError(Exception):
    '''Raise this error when the `content_file` field is not set.'''


class FileMeta(ModelBase):
    '''Metaclass for File model.'''
    class Meta:
        verbose_name = 'File'
        verbose_name_plural = 'Files'
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
    original_name = CharField(_T('Original Name'), max_length=1024)

    #: The File extension.
    original_extension = CharField(_T('Original Extension'), max_length=8, null=True, blank=True)

    #: Thumbnail extension.
    thumbnail_extension = CharField(_T('Thumbnail Extension'), max_length=8, null=True, blank=True)

    #: The File's mime type.
    mime_type = ForeignKey(to=MaioMimeType, on_delete=DO_NOTHING, editable=False)

    #: The size, in bytes, of the File.
    size = PositiveIntegerField(_T('Size (Bytes)'), default=0, editable=False)

    #: File modified date, as a Unix time stamp.
    mtime = FloatField(_T('Unix Timestamp'), default=0.0, editable=False)

    #: File modified date, as a DateTime.
    modified_time = DateTimeField(_T('Modified Time'), auto_now_add=True)

    #: The File path stored in ./filestore/media/
    content_file = FileField(_T('Content File'), max_length=1024, upload_to=maio_conf.get_chain('upload', 'directory'))

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
        content_file: UploadedFile,
    ) -> tuple[File, UploadedFile, bool]:
        '''Handle the uploaded file as given by `request.FILES`.'''
        logger = Log.new(request, 'File')
        try:
            # content_file = request.FILES.get(field)
            maio_file = File(content_file=content_file)
        except MultiValueDictKeyError as e:
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
        self.content_file.name = unidecode(self.content_file.name)
        path: str = str(os.path.join(File.content_file.field.upload_to, self.content_file.name))
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
                extensions = str(MaioMimeType.objects.get(mime_type=self.mime_type).extensions)
                extensions = extensions.split()
                if extensions:
                    ext = extensions[0]
            except MaioMimeType.DoesNotExist:
                raise
            self.original_extension = ext
        return f"{self.original_name}.{self.original_extension}"

    def set_data(self) -> bool:
        '''Set the data attributes of this object based on the uploaded file and input data.'''
        if not self.content_file:
            raise ContentFileNotSetError('`content_file` is not set.')
        now = timezone.now()
        self.size = int(self.content_file.size)
        self.mtime = now.timestamp()
        self.modified_time = now
        try:
            maio_file = File.objects.get(md5sum=self.md5sum, mime_type=self.mime_type)
            self = maio_file
        except File.DoesNotExist:
            self.save()
        return True

    def calculate_md5sum(self) -> str:
        '''Return the md5sum of the file represented by this object.'''
        # path = os.path.join(File.content_file.field.upload_to, self.content_file.name)
        # self.md5sum = hashlib.md5(open(path, 'rb').read()).hexdigest()
        self.md5sum = hashlib.md5(self.content_file.read()).hexdigest()
        return self.md5sum

    def calculate_mime_type(self) -> MaioMimeType:
        '''Return the mime type of the file represented by this object.'''
        mime: magic.Magic = magic.Magic(mime=True)
        path: str = str(os.path.join(File.content_file.field.upload_to, self.content_file.name))
        mimetype: str = str(mime.from_file(path))
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

    def load_image(self) -> tuple[Image.Image, str]:
        '''Load the image located at `self.content_file`.'''
        path: str = str(os.path.join(fs.mk_md5_dir_media(self.md5sum), self.get_filename()))
        image: Image.Image = Image.open(path)
        image.load()
        return image.copy(), path

    def process_media(self) -> bool:
        '''Process the media for this file.'''
        path: str = str(os.path.join(File.content_file.field.upload_to, self.content_file.name))
        with open(path, 'rb') as fh:
            buf = fh.read()
        root: str = fs.mk_md5_dir_media(self.md5sum)
        if root:
            file_path = os.path.join(root, self.get_filename())
            with open(file_path, 'wb') as fh:
                fh.write(buf)
            os.unlink(path)
            self.content_file = file_path
            return True
        return False

    def generate_slideshow(
        self,
        in_filename: str,
        out_filename: str,
        tn_extension: str,
    ) -> tuple[Slideshow, str]:
        '''Generate Slideshow for this File.'''
        tn_path: Optional[str] = None
        new_out_filename: str = out_filename

        # Get video length
        ffprobe_cmd = [
            maio_conf.get_ffprobe_bin_path(),
            "-show_entries", "format=duration",
            "-v", "quiet",
            "-of", "csv=p=0",
            "-i", in_filename,
        ]
        try:
            output = subprocess.run(ffprobe_cmd, capture_output=True)
            output = str(output.stdout, encoding='UTF-8')
            video_length = float(output.strip())
        except subprocess.CalledProcessError:
            raise
        # /Get video length


        # Generate Slideshow for this video.
        indexes = numpy.linspace(0.0, video_length, 22)[1:-1].tolist()
        for index, time in enumerate(indexes):
            out_filename_name = '.'.join(out_filename.split('.')[:-1])
            new_out_filename = f"{out_filename_name}_{index}.{tn_extension}"
            if not tn_path:
                tn_path = new_out_filename

            # _deets = f'''
            #     In Filename: {in_filename}
            #     Out Filename: {out_filename}
            #     Thumbnail Extension: {tn_extension}
            #     Video Length: {video_length}
            #     Indexes: {indexes}
            #     Index: {index}
            #     Time: {time}
            #     Initial Thumbnail Path: {tn_path}
            # '''
            # raise Exception(_deets)

            try:
                _any: Any = (
                    ffmpeg
                        .input(in_filename, ss=time)
                        .filter('scale', 300, -1)
                        .output(new_out_filename, vframes=1)
                        .overwrite_output()
                        .run(capture_stdout=True, capture_stderr=True)
                )
            except ffmpeg.Error as e:
                # print(e.stderr.decode(), file=sys.stderr)
                _deets = f'''
                    In Filename: {in_filename}
                    Out Filename: {out_filename}
                    Video Length: {video_length}
                    Indexes: {indexes}
                    Index: {index}
                    Time: {time}
                '''
                raise Exception(f'''
                    Error:
                    {e.stderr.decode()}
                    {_deets}
                ''')

        slideshow, ss_created = Slideshow.objects.get_or_create(file=self,
            defaults={
                'indexes': indexes,
                'num_slices': 20,
                'length': video_length,
            })
        if ss_created:
            slideshow.save()
        else:
            slideshow.indexes = indexes
            slideshow.num_slices = 20
            slideshow.length = video_length
            slideshow.save()
        # /Generate Slideshow
        return slideshow, tn_path if tn_path else ''

    def process_thumbnail(self) -> tuple[bool | str, bool]:
        '''Process the thumbnail for this file.'''
        maio_type_choice = self.mime_type.maio_type.get_choice()
        root = fs.mk_md5_dir_thumbnail(self.md5sum)
        tn_path = ''
        tn_extension = 'jpg'
        tn_uri = maio_conf.get_static_media_uri()
        is_processed = False

        if maio_type_choice == MaioTypeChoices.IMAGE:
            tn_path = os.path.join(root, self.get_filename())
            tn_extension = tn_path.split('.')[-1]
            tn_path_name = '.'.join(tn_path.split('.')[:-1])
            tn_path = f"{tn_path_name}.{tn_extension}"

            try:
                # Process JPEG thumbnails.
                # Thanks to: https://stackoverflow.com/a/6218425
                image, _image_path = self.load_image()
                orientation = None
                for orientation in ExifTags.TAGS.keys():
                    if ExifTags.TAGS[orientation] == 'Orientation':
                        break
                exif = dict(image.getexif().items())
                if orientation in exif:
                    if exif[orientation] == 3:
                        image = image.rotate(180, expand=True)
                    elif exif[orientation] == 6:
                        image = image.rotate(270, expand=True)
                    elif exif[orientation] == 8:
                        image = image.rotate(90, expand=True)
            except Exception:
                raise

            image.thumbnail((300, 300), Image.Resampling.LANCZOS)

            try:
                image.save(tn_path)
            except OSError:
                image.convert('RGB').save(tn_path)

            is_processed = True

        if maio_type_choice == MaioTypeChoices.VIDEO:
            tn_path = '.'.join(os.path.join(root, self.get_filename()).split('.')[:-1])
            tn_path = f"{tn_path}.{tn_extension}"
            in_filename = os.path.join(fs.mk_md5_dir_media(self.md5sum), self.get_filename())
            out_filename = os.path.join(fs.mk_md5_dir_slideshow(self.md5sum), self.get_filename())

            _slideshow, initial_tn_path = self.generate_slideshow(
                in_filename,
                out_filename,
                tn_extension,
            )
            tn_path = initial_tn_path

            image = Image.open(tn_path)
            image.load()
            is_processed = True

        if maio_type_choice == MaioTypeChoices.AUDIO:
            audio_tn_path = maio_conf.get_audio_thumbnail_path()
            tn_extension = audio_tn_path.split('.')[-1]
            tn_path = os.path.join(root, self.get_filename())
            tn_path_name = '.'.join(tn_path.split('.')[:-1])
            tn_path = f"{tn_path_name}.{tn_extension}"

            image = Image.open(audio_tn_path)
            image.load()

            try:
                image.save(tn_path)
            except OSError:
                image.convert('RGB').save(tn_path)

            is_processed = True

        if maio_type_choice == MaioTypeChoices.DOCUMENT:
            document_tn_path = maio_conf.get_document_thumbnail_path()
            # PDF / Adobe PDF
            if (
                self.original_extension in maio_conf.get_document_pdf_extensions() or
                self.mime_type.mime_type in maio_conf.get_document_pdf_mime_types()
            ):
                document_tn_path = maio_conf.get_document_pdf_thumbnail_path()
            # MS Word / OpenDocument Word Processing Document
            if (
                self.original_extension in maio_conf.get_document_msword_extensions() or
                self.mime_type.mime_type in maio_conf.get_document_msword_mime_types()
            ):
                document_tn_path = maio_conf.get_document_msword_thumbnail_path()
            # MS Excel / OpenDocument Spreadsheet
            if (
                self.original_extension in maio_conf.get_document_msexcel_extensions() or
                self.mime_type.mime_type in maio_conf.get_document_msexcel_mime_types()
            ):
                document_tn_path = maio_conf.get_document_msexcel_thumbnail_path()
            # MS PowerPoint / OpenDocument Presentation
            if (
                self.original_extension in maio_conf.get_document_mspowerpoint_extensions() or
                self.mime_type.mime_type in maio_conf.get_document_mspowerpoint_mime_types()
            ):
                document_tn_path = maio_conf.get_document_mspowerpoint_thumbnail_path()
            # MS Access / OpenDocument Database
            if (
                self.original_extension in maio_conf.get_document_msaccess_extensions() or
                self.mime_type.mime_type in maio_conf.get_document_msaccess_mime_types()
            ):
                document_tn_path = maio_conf.get_document_msaccess_thumbnail_path()
            # XML
            if (
                self.original_extension in maio_conf.get_document_xml_extensions() or
                self.mime_type.mime_type in maio_conf.get_document_xml_mime_types()
            ):
                document_tn_path = maio_conf.get_document_xml_thumbnail_path()
            # Text
            if (
                self.original_extension in maio_conf.get_document_text_extensions() or
                self.mime_type.mime_type in maio_conf.get_document_text_mime_types()
            ):
                document_tn_path = maio_conf.get_document_text_thumbnail_path()

            tn_extension = document_tn_path.split('.')[-1]
            tn_path = os.path.join(root, self.get_filename())
            tn_path_name = '.'.join(tn_path.split('.')[:-1])
            tn_path = f"{tn_path_name}.{tn_extension}"

            # _deets = f'''
            #     tn_extension: {tn_extension}
            #     tn_path: {tn_path}
            # '''
            # raise Exception(_deets)

            image = Image.open(document_tn_path)
            image.load()

            try:
                image.save(tn_path)
            except OSError:
                image.convert('RGB').save(tn_path)

            is_processed = True

        if is_processed:
            self.thumbnail_extension = tn_extension
            try:
                self.thumbnail, is_created = Thumbnail.objects.get_or_create(
                    file=self,
                    md5sum=self.md5sum,
                    content_file=tn_path,
                    extension=tn_extension,
                    uri=tn_uri,
                    width=image.width,
                    height=image.height,
                    size=os.stat(tn_path).st_size,
                )
            except IntegrityError:
                self.thumbnail = Thumbnail.objects.get(md5sum=self.md5sum)
                is_created = False
            finally:
                image.close()
            return tn_path, is_created
        else:
            raise Exception(f"Mime Type: {self.mime_type}")

        return self.get_thumbnail_path(), False

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

    def get_tn_filename(self) -> str:
        '''Generate the thumbnail filename of this file.'''
        if self.thumbnail_extension:
            return f"{self.md5sum}.{self.thumbnail_extension}"
        return self.md5sum

    def get_media_path(self) -> str:
        '''Return the filesystem file path.'''
        return self.content_file.path

    def get_thumbnail_path(self) -> str:
        '''Return the filesystem thumbnail path.'''
        root = fs.mk_md5_dir_thumbnail(self.md5sum)
        path = os.path.join(root, self.get_filename())
        return path
