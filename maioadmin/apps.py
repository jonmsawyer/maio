'''
File: apps.py

Module: ``maioadmin.apps``
'''

from __future__ import annotations

from django.apps import AppConfig


class MaioAdminAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'maioadmin'
