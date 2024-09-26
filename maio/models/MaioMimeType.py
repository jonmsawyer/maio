'''
File: MaioMimeType.py

Module: ``maio.models.MaioMimeType``
'''

from __future__ import annotations

import os
import uuid

from django.conf import settings
from django.utils import timezone
from django.db.models import Model, UUIDField, CharField, ForeignKey, DO_NOTHING
from django.db.models.base import ModelBase

from .MaioType import MaioType, MaioTypeChoices


class MaioMimeTypeMeta(ModelBase):
    '''Metaclass for MaioType model.'''
    class Meta:
        verbose_name = 'Maio Mime Type'
        verbose_name_plural = 'Maio Mime Types'
        app_label = 'maio'
        db_table_comment = 'General Maio Mime Types.'
        # get_latest_by = ['-date_modified']
        # order_with_respect_to = ['maio_type']
        # ordering = ['mime_type']
        # indexes = [
        #     Index(fields=('sort', 'name', 'is_default', 'date_added', '-date_modified'))
        # ]


class MaioMimeType(Model, metaclass=MaioMimeTypeMeta):
    '''MaioType model.'''
    id = UUIDField('UUID', primary_key=True, default=uuid.uuid4, editable=False)
    maio_type = ForeignKey(to=MaioType, on_delete=DO_NOTHING, default=MaioType.default)
    mime_type = CharField('Mime Type', max_length=254, unique=True)
    extensions = CharField('Extensions', max_length=254, null=True, blank=True)

    def __str__(self) -> str:
        return self.mime_type

    @staticmethod
    def load_mimetype_data() -> None:
        '''Load mimetype data from `./data/mime.types`.'''
        with open(os.path.join(settings.BASE_DIR, 'data', 'mime.types'), 'r') as fh:
            buf = fh.read()

        mimetypes = []
        mime_to_type = {
            'application': MaioTypeChoices.DOCUMENT,
            'document': MaioTypeChoices.DOCUMENT,
            'audio': MaioTypeChoices.AUDIO,
            'image': MaioTypeChoices.IMAGE,
            'text': MaioTypeChoices.DOCUMENT,
            'video': MaioTypeChoices.VIDEO,
            'other': MaioTypeChoices.OTHER,
        }

        lines = buf.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('#'):
                continue
            parts = line.split()
            try:
                # If the line looks like this: `image/png   image    png`, then this is from the
                # new format.
                if parts[1] in mime_to_type:
                    maio_type = MaioType.objects.get_or_create(maio_type=parts[1])[0]
                    mimetypes.append((parts[0], maio_type, ' '.join(parts[2:])))
                # If the line looks like this: `image/png    png`, then this is from the old
                # format.
                else:
                    mime = parts[0].split('/')[0]
                    maio_type = MaioType.objects.get_or_create(
                        maio_type=mime_to_type.get(mime, MaioTypeChoices.OTHER)
                    )[0]
                    mimetypes.append((parts[0], maio_type, ' '.join(parts[1:])))
            except IndexError:
                continue

        for m_type in mimetypes:
            # raise Exception(f"{type(maio_type)}")
            MaioMimeType.objects.get_or_create(
                mime_type=m_type[0],
                maio_type=m_type[1],
                extensions=m_type[2],
            )
            print(f"Mimetype `{m_type[0]}` with Maio Type `{m_type[1]}` with extensions `{m_type[2]}` loaded.")

    @staticmethod
    def dump_mimetype_data():
        '''Dump the mimetype data from the db into `./data/mime.types`.'''
        now = timezone.now()
        mimetypes = []
        longest_mime_type = 0
        longest_maio_type = 0
        longest_extensions = 0
        buf = f'''# This file maps Internet media types to unique file extension(s).
# Although created for httpd, this file is used by many software systems
# and has been placed in the public domain for unlimited redisribution.
#
# The table below contains both registered and (common) unregistered types.
# A type that has no unique extension can be ignored -- they are listed
# here to guide configurations toward known types and to make it easier to
# identify "new" types.  File extensions are also commonly used to indicate
# content languages and encodings, so choose them carefully.
#
# Internet media types should be registered as described in RFC 4288.
# The registry is at <http://www.iana.org/assignments/media-types/>.
#
# Data dumped by Maio on: {now}
#
'''
        maio_mime_types = MaioMimeType.objects.all().order_by('mime_type')
        for mime_type in maio_mime_types:
            mimetypes.append((mime_type.mime_type, mime_type.maio_type, mime_type.extensions))
            if len(mime_type.mime_type) > longest_mime_type:
                longest_mime_type = len(mime_type.mime_type)
            if len(mime_type.maio_type.maio_type) > longest_maio_type:
                longest_maio_type = len(mime_type.maio_type.maio_type)
            if len(mime_type.extensions) > longest_extensions:
                longest_extensions = len(mime_type.extensions)

        header = ('MIME type (lowercased)', 'Maio Type', 'Extensions')
        buf += f"# {header[0]:<{longest_mime_type-2}}    {header[1]:<{longest_maio_type}}   {header[2]}\n"
        buf += "# " + "="*(longest_mime_type-2) + "    " + "="*longest_maio_type + "    " + "="*longest_extensions + "\n"

        for mime_type, maio_type, extensions in mimetypes:
            buf += f"{mime_type:<{longest_mime_type}}    {maio_type.maio_type:<{longest_maio_type}}    {extensions}\n"

        with open(os.path.join(settings.BASE_DIR, 'data', 'mime.types'), 'w') as fh:
            fh.write(buf)

        print("MIME type data has been dumped from the database to `./data/mime.types`.")

    def get_maio_type_choice(self):
        '''Get the MaioTypeChoices variant of this mime type.'''
        return self.maio_type.get_choice()
