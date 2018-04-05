from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from maio.models import Media

@login_required
def dashboard(request):
    cd = {}
    width = 260
    cd['images'] = Media.get_all_images(request)
    cd['width'] = width
    for image in cd['images']:
        if image.width > image.height:
            image.margin_left = width - int(image.width)
            image.margin_top = 0
        else:
            image.margin_top = width - int(image.height)
            image.margin_left = 0
    raise Exception(image.margin_left, image.margin_top, image.width, image.height)
    return render(request, 'maio/dashboard.html', cd)
