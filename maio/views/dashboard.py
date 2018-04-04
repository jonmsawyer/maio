from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from maio.models import ImageFile

@login_required
def dashboard(request):
    cd = {}
    images = ImageFile.objects.filter(owner=request.user)[0:50]
    cd['images'] = images
    return render(request, 'maio/dashboard.html', cd)
