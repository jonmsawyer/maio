'''
:file: dashboard.py
:module: ``maio.views.dashboard``
'''

# pylint:

import logging
import time
from datetime import datetime

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from maio.models import Media

logger = logging.getLogger('maio.DEBUG')
logger.debug('============================================')
logger.debug('Logger start: {}'.format(datetime.now()))
logger.debug('============================================')

def get_pagination(request, items, per_page):
    spread = 6
    paginator = Paginator(items, per_page)
    page = request.GET.get('page')
    pages = paginator.get_page(page)
    page_range_first = pages.number - spread
    if page_range_first < 0:
        page_range_first = 0
    page_range_last = pages.number + spread
    page_range = list(paginator.page_range)[page_range_first:page_range_last]
    pages.paginator.custom_page_range = page_range
    return pages

@login_required
def dashboard(request):
    cd = {}
    width = 260
    images_list = Media.get_all_images(request)
    try:
        per_page = int(request.GET.get('per_page', 28))
    except:
        per_page = 28
    images = get_pagination(request, images_list, per_page)
    for image in images:
        logger.debug('  processing image: {} (time={})'.format(image, time.time()))
        if image.tn_width > image.tn_height:
            x = width * image.tn_width / image.tn_height
            margin = int(width - x) // 2
            image.margin_left = margin
            image.margin_top = 0
        else:
            y = width * image.tn_height / image.tn_width
            margin = int(width - y) // 2
            image.margin_top = margin
            image.margin_left = 0
    cd['width'] = width
    cd['images'] = images
    cd['pages'] = images # for pagination
    cd['per_page'] = per_page
    return render(request, 'maio/dashboard.html', cd)
