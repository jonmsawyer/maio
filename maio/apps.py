'''
File: apps.py

Module: ``maio.apps``
'''

from __future__ import annotations

from django.apps import AppConfig


class MaioAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'maio'
