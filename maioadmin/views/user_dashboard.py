'''
File: dashboard.py

Module: ``maio.views.dashboard``
'''

from __future__ import annotations
from typing import Optional

import logging
# import time
from datetime import datetime

from django.http import HttpRequest, HttpResponse, Http404
# from django.shortcuts import render
# from django.core.paginator import Page, Paginator
# from django.db.models import QuerySet
# from django.urls import reverse

# from maio.lib import pre_populate_context_dict
# from maio.models import Media
from maio.views import dashboard


logger = logging.getLogger('maio.DEBUG')
logger.debug('=================================================================')
logger.debug('Maio Admin User Dashboard Logger start: {}'.format(datetime.now()))
logger.debug('=================================================================')


def user_dashboard(request: HttpRequest, username: str) -> HttpResponse:
    if not request.user.is_superuser:
        raise Http404()
    return dashboard(request, with_username=username)
