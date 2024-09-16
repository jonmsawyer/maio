'''
File: dashboard.py

Module: ``maio.views.dashboard``
'''

from __future__ import annotations
# from typing import Any

import json
from re import M
# import logging
# import time
# from datetime import datetime

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# from django.core.paginator import Page, Paginator
# from django.db.models import QuerySet

from maio.lib import pre_populate_context_dict
from maio.models import File, Media

# logger = logging.getLogger('maio.DEBUG')
# logger.debug('============================================')
# logger.debug('Logger start: {}'.format(datetime.now()))
# logger.debug('============================================')

# def get_pagination(request: HttpRequest, items: QuerySet[Any], per_page: int | str) -> Page:
#     spread = 6
#     paginator = Paginator(items, per_page)
#     page = request.GET.get('page')
#     pages = paginator.get_page(page)
#     page_range_first = pages.number - spread
#     if page_range_first < 0:
#         page_range_first = 0
#     page_range_last = pages.number + spread
#     page_range = list(paginator.page_range)[page_range_first:page_range_last]
#     pages.paginator.custom_page_range = page_range # type: ignore[reportGeneralTypeIssues]
#     return pages

@login_required
def delete_media(request: HttpRequest) -> JsonResponse:
    '''Delete the Media for this user for a given UUID.'''
    # cd = pre_populate_context_dict(request, {})

    if request.method == 'POST':
        media_uuid = request.POST.get('media_uuid');
        delete_all = False
        media_deleted = []
        ret = None
        if request.user.is_superuser:
            delete_all = request.POST.get('delete_all')
            if delete_all == 'true':
                delete_all = True
            else:
                delete_all = False
        media = Media.objects.get(pk=media_uuid)
        if delete_all:
            f = media.file
            for med in f.media_set.all():
                media_deleted.append(med.id)
            ret = f.delete()
        else:
            media_deleted.append(media.id)
            ret = media.delete()
    return JsonResponse({
        'delete_media_uuid': media_uuid,
        'delete_all': delete_all,
        'deleted_media': media_deleted,
        'ret': ret,
    })
