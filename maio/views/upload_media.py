'''
File: dashboard.py

Module: ``maio.views.dashboard``
'''

from __future__ import annotations
from typing import Any

# from django.urls import reverse
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
# from django.contrib.auth.models import User
# from django.contrib.auth.decorators import login_required
# from django.core.files.uploadedfile import UploadedFile
from django.views.generic.edit import FormView

from maio.forms import FileForm
from maio.models import File, Media
from maio.lib import pre_populate_context_dict

class UploadMediaView(FormView):
    form_class = FileForm
    template_name = 'maio/upload_media.html'
    success_url = '/upload_media/'

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        cd = pre_populate_context_dict(request, {
            'form': FileForm(request.POST, request.FILES),
            'media': {
                'new': [],
                'new_count': 0,
                'old': [],
                'old_count': 0,
            },
        })
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('content_file')
        if form.is_valid():
            data = form.cleaned_data
            for f in files:
                maio_file, content_file, _is_created = File.handle_uploaded_file(request, content_file=f)
                num_media = Media.objects.filter(file=maio_file).count()
                if num_media > 0 and data.get('skip_duplicates', True):
                    try:
                        cd['media']['old'].append(maio_file.media_set.filter(owner=request.user)[0])
                        cd['media']['old_count'] += 1
                        continue
                    except IndexError:
                        pass

                media_file = Media.create_from_maio_file(request, maio_file, content_file)
                cd['media']['new'].append(media_file)
                cd['media']['new_count'] += 1
        context = super(UploadMediaView, self).get_context_data(**cd)
        return render(request, self.template_name, context)
