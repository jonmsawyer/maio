from django.shortcuts import render

from maio.models import ImageFile


def home(request):
    cd ={'images': ImageFile.objects.all()[0:300]}
    return render(request, 'maio/home.html', cd)
