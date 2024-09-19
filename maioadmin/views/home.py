'''
File: home.py

Module: ``maio.views.maio_admin.home``
'''

from __future__ import annotations

from django.shortcuts import render
# from django.shortcuts import redirect
from django.http import (
    HttpRequest, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect,
)
from django.contrib.auth.models import User

# from maio.forms import LoginForm
from maio.lib import pre_populate_context_dict


def home(
    request: HttpRequest
) -> HttpResponseRedirect | HttpResponsePermanentRedirect | HttpResponse:
    if not request.user.is_superuser:
        raise Http404()
    cd = pre_populate_context_dict(request, {})
    cd['user_list'] = User.objects.all().order_by('id')
    return render(request, 'maio_admin/home.html', cd)
