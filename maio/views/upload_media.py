'''
File: dashboard.py

Module: ``maio.views.dashboard``
'''

from __future__ import annotations
from typing import Any

# from django.urls import reverse
from django.conf import settings
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
# from django.contrib.auth.models import User
# from django.contrib.auth.decorators import login_required
# from django.core.files.uploadedfile import UploadedFile
from django.views.generic.edit import FormView
from django.utils.safestring import mark_safe

from maio.forms import FileForm
from maio.models import File, Media
from maio.lib import pre_populate_context_dict

from conf import MaioConf


maio_conf = MaioConf(settings.MAIO_SETTINGS)


def _get_context(request: HttpRequest) -> dict[str, Any]:
    '''get context'''
    js_debug = 'true' if request.user.is_superuser and request.user_setting.display_debug else 'false'
    render_div_index = 'true' if request.user.is_superuser and request.user_setting.display_debug else 'false'
    context = {
        'js_debug': js_debug,
        'render_div_index': render_div_index,
        'form': FileForm(request.POST, request.FILES),
        'restricted_extensions': mark_safe(maio_conf.get_chain('upload', 'restricted', 'extensions')),
        'restricted_mime_types': mark_safe(maio_conf.get_chain('upload', 'restricted', 'mime_types')),
        'preview_view': request.user_setting.default_upload_media_view or 'default',
        'media': {
            'new': [],
            'new_count': 0,
            'old': [],
            'old_count': 0,
        },
    }
    return pre_populate_context_dict(request, context)

class UploadMediaView(FormView):
    form_class = FileForm
    template_name = 'maio/upload_media.html'
    success_url = '/upload_media/'

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse | JsonResponse:
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('content_file')
        cd = _get_context(request)
        if form.is_valid():
            data = form.cleaned_data
            for f in files:
                maio_file, content_file, _is_created = File.handle_uploaded_file(request, content_file=f)
                num_media = Media.objects.filter(file=maio_file).count()
                if num_media > 0 and data.get('skip_duplicates', True):
                    try:
                        cd['media']['old'].append(maio_file.media_set.filter(owner=request.user)[0])
                        cd['media']['old_count'] += 1
                        if request.POST.get('from_ajax', False):
                            return JsonResponse({
                                'status': 'OK',
                                'is_duplicate': True,
                                'file_index': request.POST.get('file_index'),
                            })
                        continue
                    except IndexError:
                        pass

                media_file = Media.create_from_maio_file(request, maio_file, content_file)
                cd['media']['new'].append(media_file)
                cd['media']['new_count'] += 1
                if request.POST.get('from_ajax', False):
                    return JsonResponse({
                        'status': 'OK',
                        'is_duplicate': False,
                        'file_index': request.POST.get('file_index'),
                    })
        if request.POST.get('from_ajax', False):
            return JsonResponse({
                'status': 'Error',
                'reason': 'Form is not valid.',
                'file_index': request.POST.get('file_index'),
            })
        context = super(UploadMediaView, self).get_context_data(**cd)
        return render(request, self.template_name, context)

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        cd = _get_context(request)
        context = super(UploadMediaView, self).get_context_data(**cd)
        return render(request, self.template_name, context)
