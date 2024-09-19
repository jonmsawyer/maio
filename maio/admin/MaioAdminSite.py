'''
File: MaioAdminSite.py

Module: ``maio.admin.MaioAdminSite``
'''

from __future__ import annotations

from django.contrib.admin import AdminSite


class MaioAdminSite(AdminSite):
    '''Maio Admin Site'''
    site_title = 'Maio Administration'
    site_header = 'Maio Administration'
