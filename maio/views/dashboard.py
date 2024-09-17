'''
File: dashboard.py

Module: ``maio.views.dashboard``
'''

from __future__ import annotations
from typing import Any

import logging
import time
from datetime import datetime

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Page, Paginator
from django.db.models import QuerySet
from django.urls import reverse

from maio.lib import pre_populate_context_dict
from maio.models import Media

logger = logging.getLogger('maio.DEBUG')
logger.debug('============================================')
logger.debug('Logger start: {}'.format(datetime.now()))
logger.debug('============================================')

def get_pagination(request: HttpRequest, items: QuerySet[Any], per_page: int | str) -> Page:
    spread = 6
    paginator = Paginator(items, per_page)
    page = request.GET.get('page')
    pages = paginator.get_page(page)
    page_range_first = pages.number - spread
    if page_range_first < 0:
        page_range_first = 0
    page_range_last = pages.number + spread
    page_range = list(paginator.page_range)[page_range_first:page_range_last]
    pages.paginator.custom_page_range = page_range # type: ignore[reportGeneralTypeIssues]
    return pages

@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    cd = pre_populate_context_dict(request, {})
    width = 260
    media_type = request.GET.get('media_type', 'all')
    if media_type not in ('all', 'image', 'audio', 'video', 'document', 'other'):
        media_type = 'all'
    if media_type == 'image':
        media_list = Media.get_all_images(request)
    elif media_type == 'audio':
        media_list = Media.get_all_audio(request)
    elif media_type == 'video':
        media_list = Media.get_all_videos(request)
    elif media_type == 'document':
        media_list = Media.get_all_documents(request)
    else:
        media_list = Media.get_all_media(request)
    try:
        per_page = int(request.GET.get('per_page', 28))
    except:
        per_page = 28
    media = get_pagination(request, media_list, per_page)
    for medium in media:
        logger.debug('  processing image: {} (time={})'.format(medium, time.time()))
        if medium.tn_width > medium.tn_height:
            x = width * medium.tn_width / medium.tn_height
            margin = int(width - x) // 2
            medium.margin_left = margin
            medium.margin_top = 0
        else:
            y = width * medium.tn_height / medium.tn_width
            margin = int(width - y) // 2
            medium.margin_top = margin
            medium.margin_left = 0

    # Set up query_dict
    qd = request.GET.copy()
    qd['media_type'] = media_type
    qd['per_page'] = per_page
    # /query_dict

    cd['query_dict'] = qd
    cd['width'] = width
    cd['image_height'] = 800
    cd['image_width'] = 1100
    cd['media_type'] = media_type
    cd['media'] = media
    cd['num_media'] = media_list.count()
    cd['pages'] = media # for pagination
    cd['per_page'] = per_page
    cd['delete_media_url'] = reverse('delete_media')
    return render(request, 'maio/dashboard.html', cd)
