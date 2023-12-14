'''
File: MaioAdminSite.py

Module: ``maio.admin.MaioAdminSite``
'''

from __future__ import annotations

from django.contrib.admin import AdminSite


class MaioAdminSite(AdminSite):
    site_header = 'Maio Administration'
    site_title = 'Maio Administration'
