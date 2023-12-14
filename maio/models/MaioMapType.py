'''
File: MaioMapType.py

Module: ``maio.models.MaioMapType``
'''

from __future__ import annotations

import uuid
from uuid import UUID

from django.db.models import (
    Model, UUIDField, CharField, TextChoices,
)
from django.db.models.base import ModelBase
from django.utils.translation import gettext_lazy as _T


class MaioMapTypeChoices(TextChoices):
    '''Text choices class for the MaioMap model's `maio_type` field.'''
    NULL = 'null', _T('Null/None (NULL)')
    BOOL = 'bool', _T('Boolean (Number)')
    NULL_BOOL = 'null_bool', _T('Null Boolean (Number/None)')
    INT = 'int', _T('Integer (Number)')
    BIG_INT = 'big_int', _T('Big Integer (Number)')
    SMALL_INT = 'small_int', _T('Small Integer (Number)')
    POS_INT = 'pos_int', _T('Positive Integer (Number)')
    POS_BIG_INT = 'pos_big_int', _T('Positive Big Integer (Number)')
    POS_SMALL_INT = 'pos_small_int', _T('Positive Small Integer (Number)')
    CS_INT = 'cs_int', _T('Comma Separated Integer (String)')
    FLOAT = 'float', _T('Float (Number)')
    DECIMAL = 'decimal', _T('Decimal (Number)')
    DURATION = 'duration', _T('Duration (Number)')
    AUTO = 'auto', _T('Auto (Number)')
    BIG_AUTO = 'big_auto', _T('Big Auto (Number)')
    SMALL_AUTO = 'small_auto', _T('Small Auto (Number)')
    STRING = 'string', _T('String')
    UUID = 'uuid', _T('UUID (String)')
    DATE = 'date', _T('Date (String)')
    TIME = 'time', _T('Time (String)')
    DATETIME = 'datetime', _T('Date Time (String)')
    DATETIME_TZ = 'datetime_tz', _T('Date Time w/ Time Zone (String)'),
    JSON = 'json', _T('JSON (String)')
    XML = 'xml', _T('XML (String)')
    MD = 'markdown', _T('Markdown (String)')
    IPV4 = 'ipv4', _T('IPv4 (String)')
    IPV6 = 'ipv6', _T('IPv6 (String)')
    MAC_ADDRESS = 'mac_address', _T('MAC Address (String)')
    URL = 'url', _T('URL (String)')
    EMAIL = 'email', _T('Email Address (String)')
    PASSWORD = 'password', _T('Password (Encrypted String)')
    TEXT = 'text', _T('Text')
    FILE_PATH = 'file_path', _T('File Path (String)')
    SLUG = 'slug', _T('Slug')
    BINARY = 'binary', _T('Binary (Number)')
    HEX = 'hex', _T('Hexidecimal (Number)')
    OCTAL = 'octal', _T('Octal (Number)')
    REGEX_PATTERN = 'regex_pattern', _T('Regex Pattern (String)')
    US_PHONE_NUMBER = 'us_phone_number', _T('US Phone Number (String)')
    INTL_PHONE_NUMBER = 'intl_phone_number', _T('International Phone Number (String)')


class MaioMapTypeMeta(ModelBase):
    '''Metaclass for MaioType model.'''
    name = 'Maio Map Type'
    verbose_name = 'Maio Map Types'
    app_label = 'maio'
    db_table_comment = 'General Maio Map Types.'
    # get_latest_by = ['-date_modified']
    # order_with_respect_to = ['']
    ordering = ['maio_map_type']


class MaioMapType(Model, metaclass=MaioMapTypeMeta):
    '''MaioType model.'''
    id = UUIDField('UUID', primary_key=True, default=uuid.uuid4, editable=False)
    maio_map_type = CharField('Maio Map Type', max_length=20, choices=MaioMapTypeChoices.choices, unique=True)

    def __str__(self) -> str:
        return self.maio_map_type

    @staticmethod
    def default() -> UUID:
        '''Return the defau't MaioType.'''
        MaioMapType.objects.get_or_create(maio_map_type=MaioMapTypeChoices.NULL)
        MaioMapType.objects.get_or_create(maio_map_type=MaioMapTypeChoices.BOOL)
        MaioMapType.objects.get_or_create(maio_map_type=MaioMapTypeChoices.NULL_BOOL)
        MaioMapType.objects.get_or_create(maio_map_type=MaioMapTypeChoices.INT)
        MaioMapType.objects.get_or_create(maio_map_type=MaioMapTypeChoices.BIG_INT)
        MaioMapType.objects.get_or_create(maio_map_type=MaioMapTypeChoices.SMALL_INT)
        MaioMapType.objects.get_or_create(maio_map_type=MaioMapTypeChoices.POS_INT)
        MaioMapType.objects.get_or_create(maio_map_type=MaioMapTypeChoices.POS_BIG_INT)
        MaioMapType.objects.get_or_create(maio_map_type=MaioMapTypeChoices.POS_SMALL_INT)
        MaioMapType.objects.get_or_create(maio_map_type=MaioMapTypeChoices.CS_INT)
        MaioMapType.objects.get_or_create(maio_map_type=MaioMapTypeChoices.FLOAT)
        MaioMapType.objects.get_or_create(maio_map_type=MaioMapTypeChoices.DECIMAL)
        MaioMapType.objects.get_or_create(maio_map_type=MaioMapTypeChoices.DURATION)
        MaioMapType.objects.get_or_create(maio_map_type=MaioMapTypeChoices.AUTO)
        MaioMapType.objects.get_or_create(maio_map_type=MaioMapTypeChoices.BIG_AUTO)
        MaioMapType.objects.get_or_create(maio_map_type=MaioMapTypeChoices.SMALL_AUTO)
        MaioMapType.objects.get_or_create(maio_map_type=MaioMapTypeChoices.UUID)
        MaioMapType.objects.get_or_create(maio_map_type=MaioMapTypeChoices.DATE)
        MaioMapType.objects.get_or_create(maio_map_type=MaioMapTypeChoices.TIME)
        MaioMapType.objects.get_or_create(maio_map_type=MaioMapTypeChoices.DATETIME)
        MaioMapType.objects.get_or_create(maio_map_type=MaioMapTypeChoices.DATETIME_TZ)
        MaioMapType.objects.get_or_create(maio_map_type=MaioMapTypeChoices.JSON)
        MaioMapType.objects.get_or_create(maio_map_type=MaioMapTypeChoices.XML)
        MaioMapType.objects.get_or_create(maio_map_type=MaioMapTypeChoices.MD)
        MaioMapType.objects.get_or_create(maio_map_type=MaioMapTypeChoices.IPV4)
        MaioMapType.objects.get_or_create(maio_map_type=MaioMapTypeChoices.IPV6)
        MaioMapType.objects.get_or_create(maio_map_type=MaioMapTypeChoices.MAC_ADDRESS)
        MaioMapType.objects.get_or_create(maio_map_type=MaioMapTypeChoices.URL)
        MaioMapType.objects.get_or_create(maio_map_type=MaioMapTypeChoices.EMAIL)
        MaioMapType.objects.get_or_create(maio_map_type=MaioMapTypeChoices.PASSWORD)
        MaioMapType.objects.get_or_create(maio_map_type=MaioMapTypeChoices.TEXT)
        MaioMapType.objects.get_or_create(maio_map_type=MaioMapTypeChoices.FILE_PATH)
        MaioMapType.objects.get_or_create(maio_map_type=MaioMapTypeChoices.SLUG)
        MaioMapType.objects.get_or_create(maio_map_type=MaioMapTypeChoices.BINARY)
        MaioMapType.objects.get_or_create(maio_map_type=MaioMapTypeChoices.HEX)
        MaioMapType.objects.get_or_create(maio_map_type=MaioMapTypeChoices.OCTAL)
        MaioMapType.objects.get_or_create(maio_map_type=MaioMapTypeChoices.REGEX_PATTERN)
        MaioMapType.objects.get_or_create(maio_map_type=MaioMapTypeChoices.US_PHONE_NUMBER)
        MaioMapType.objects.get_or_create(maio_map_type=MaioMapTypeChoices.INTL_PHONE_NUMBER)
        maio_map_type, _created = MaioMapType.objects.get_or_create(maio_map_type=MaioMapTypeChoices.STRING)
        return maio_map_type.id
