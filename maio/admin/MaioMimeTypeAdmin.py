'''
File: MaioMimeTypeAdmin.py

Module: ``maio.admin.MaioMimeTypeAdmin``
'''

from __future__ import annotations
from typing import Any

from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.http import HttpRequest
from django.db.models import QuerySet

from maio.models import MaioMimeType, MaioType, MaioTypeChoices


@admin.action(description='Set selected to `image` Maio Type.')
def make_image_type(
    modeladmin: Any,
    request: HttpRequest,
    queryset: QuerySet[MaioMimeType],
) -> None:
    maio_type_image, _created = MaioType.objects.get_or_create(maio_type=MaioTypeChoices.IMAGE)
    queryset.update(maio_type=maio_type_image)

@admin.action(description='Set selected to `audio` Maio Type.')
def make_audio_type(
    modeladmin: Any,
    request: HttpRequest,
    queryset: QuerySet[MaioMimeType],
) -> None:
    maio_type_audio, _created = MaioType.objects.get_or_create(maio_type=MaioTypeChoices.AUDIO)
    queryset.update(maio_type=maio_type_audio)

@admin.action(description='Set selected to `video` Maio Type.')
def make_video_type(
    modeladmin: Any,
    request: HttpRequest,
    queryset: QuerySet[MaioMimeType],
) -> None:
    maio_type_video, _created = MaioType.objects.get_or_create(maio_type=MaioTypeChoices.VIDEO)
    queryset.update(maio_type=maio_type_video)

@admin.action(description='Set selected to `document` Maio Type.')
def make_document_type(
    modeladmin: Any,
    request: HttpRequest,
    queryset: QuerySet[MaioMimeType],
) -> None:
    maio_type_document, _created = MaioType.objects.get_or_create(maio_type=MaioTypeChoices.DOCUMENT)
    queryset.update(maio_type=maio_type_document)

@admin.action(description='Set selected to `other` Maio Type.')
def make_other_type(
    modeladmin: Any,
    request: HttpRequest,
    queryset: QuerySet[MaioMimeType],
) -> None:
    maio_type_other, _created = MaioType.objects.get_or_create(maio_type=MaioTypeChoices.OTHER)
    queryset.update(maio_type=maio_type_other)


class MaioMimeTypeAdmin(ModelAdmin): # type: ignore[reportMissingTypeArgument]
    list_display = ['maio_type', 'mime_type', 'extensions']
    list_filter = ['maio_type']
    search_fields = ['mime_type', 'extensions']
    actions = [
        make_image_type,
        make_audio_type,
        make_video_type,
        make_document_type,
        make_other_type,
    ]
