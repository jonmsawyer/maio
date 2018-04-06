from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from maio.models import Media

@login_required
def dashboard(request):
    cd = {}
    width = 260
    images = list(Media.get_all_images(request))
    for image in images:
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
    cd['width'] = 260
    cd['images'] = images
    return render(request, 'maio/dashboard.html', cd)
