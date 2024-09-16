'''
File: dashboard.py

Module: ``maio.views.dashboard``
'''

from __future__ import annotations

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# from django.core.files.uploadedfile import UploadedFile

from maio.forms import FileForm
from maio.models import File, Media
from maio.lib import pre_populate_context_dict

@login_required
def upload_media(request: HttpRequest) -> HttpResponse:
    cd = pre_populate_context_dict(
        request,
        {
            'form': FileForm(request.POST, request.FILES),
            'media': None,
        }
    )
    if request.method == 'POST':
        if cd['form'].is_valid():
            maio_file, content_file, _is_created = File.handle_uploaded_file(request, 'content_file')
            cd['media'] = Media.create_from_maio_file(request, maio_file, content_file)
        else:
            raise Exception('form is not valid')
    return render(request, 'maio/upload_media.html', cd)
