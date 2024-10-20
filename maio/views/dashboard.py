'''
File: dashboard.py

Module: ``maio.views.dashboard``
'''

from __future__ import annotations
from typing import Any, Optional

import logging
import time
from datetime import datetime

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Page, Paginator
from django.db.models import QuerySet

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


def sanitize_filter_media_type(media_type: str) -> str:
    '''validate_filter_media_type'''
    if media_type not in ('all', 'image', 'audio', 'video', 'document', 'other'):
        media_type = 'all'
    return media_type


def sanitize_filter_love(love: str) -> str:
    '''validate_filter_media_type'''
    if love not in ('all', 'loved', 'unloved'):
        love = 'all'
    return love


def sanitize_filter_bookmark(bookmark: str) -> str:
    '''validate_filter_media_type'''
    if bookmark not in ('all', 'bookmarked', 'unbookmarked'):
        bookmark = 'all'
    return bookmark


@login_required
def dashboard(request: HttpRequest, with_username: Optional[str] = None, is_admin: Optional[bool] = None) -> HttpResponse:
    cd = pre_populate_context_dict(request, {})

    with_user = None
    if with_username:
        try:
            with_user = User.objects.get(username=with_username)
        except User.DoesNotExist:
            pass

    width = 260
    media_type = sanitize_filter_media_type(request.GET.get('media_type', 'all'))
    love = sanitize_filter_love(request.GET.get('love', 'all'))
    bookmark = sanitize_filter_bookmark(request.GET.get('bookmark', 'all'))
    media_list = Media.get_all_by_media_type(request, media_type, with_user, love, bookmark)
    try:
        per_page = int(request.GET.get('per_page', request.user_setting.default_dashboard_per_page))
    except:
        per_page = request.user_setting.default_dashboard_per_page
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
        medium.is_loved = medium.is_loved_by(request.maio_user)
        medium.is_bookmarked = medium.is_bookmarked_by(request.maio_user)

    # Set up query_dict
    qd = request.GET.copy()
    qd['media_type'] = media_type
    qd['love'] = love
    qd['bookmark'] = bookmark
    qd['per_page'] = per_page
    # /query_dict

    cd['js_debug'] = 'true'
    cd['is_admin'] = is_admin
    cd['with_user'] = with_user
    cd['query_dict'] = qd
    cd['width'] = width
    cd['image_height'] = 800
    cd['image_width'] = 1100
    cd['media_type'] = media_type
    cd['love'] = love
    cd['bookmark'] = bookmark
    cd['media'] = media
    cd['num_media'] = media_list.count()
    cd['pages'] = media # for pagination
    cd['per_page'] = per_page
    return render(request, 'maio/dashboard.html', cd)
