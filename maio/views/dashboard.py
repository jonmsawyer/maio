from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from maio.models import Media

@login_required
def dashboard(request):
    cd = {}
    cd['images'] = list(Media.get_all_images(request))
    return render(request, 'maio/dashboard.html', cd)
