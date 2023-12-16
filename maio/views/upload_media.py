'''
File: dashboard.py

Module: ``maio.views.dashboard``
'''

from __future__ import annotations

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from maio.forms import FileForm
from maio.models import File


@login_required
def upload_media(request: HttpRequest) -> HttpResponse:
    cd = {
        'form': FileForm(request.POST, request.FILES),
    }
    if request.method == 'POST':
        if cd['form'].is_valid():
            File.handle_uploaded_file(request, 'content_file')
            cd['form'].save()
            #raise Exception(f"form: {dir(cd['form'])}")
        else:
            raise Exception('form is not valid')
    return render(request, 'maio/upload_media.html', cd)
