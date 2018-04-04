from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from maio.models import ImageFile

@login_required
def dashboard(request):
    cd = {}
    images = list(ImageFile.objects.filter(owner=request.user))
    images = images[-50:]
    cd['images'] = images
    return render(request, 'maio/dashboard.html', cd)
