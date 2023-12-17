'''
File: MaioMimeTypeAdmin.py

Module: ``maio.admin.MaioMimeTypeAdmin``
'''

from __future__ import annotations

from django.contrib.admin import ModelAdmin


class MaioMimeTypeAdmin(ModelAdmin): # type: ignore[reportMissingTypeArgument]
    list_display = ['maio_type', 'mime_type', 'extensions']
    list_filter = ['maio_type']
    search_fields = ['mime_type', 'extensions']
