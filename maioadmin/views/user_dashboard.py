'''
File: user_dashboard.py

Module: ``maioadmin.views.user_dashboard``
'''

from __future__ import annotations

import logging
from datetime import datetime

from django.http import HttpRequest, HttpResponse, Http404

from maio.views import dashboard


logger = logging.getLogger('maio.DEBUG')
logger.debug('=================================================================')
logger.debug('Maio Admin User Dashboard Logger start: {}'.format(datetime.now()))
logger.debug('=================================================================')


def user_dashboard(request: HttpRequest, username: str) -> HttpResponse:
    if not request.user.is_superuser:
        raise Http404()
    return dashboard(request, with_username=username, is_admin=True)
