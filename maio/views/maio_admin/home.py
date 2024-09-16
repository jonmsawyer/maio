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
# from django.contrib.auth import authenticate
# from django.contrib.auth import login

# from maio.forms import LoginForm
from maio.lib import pre_populate_context_dict

def home(
    request: HttpRequest
) -> HttpResponseRedirect | HttpResponsePermanentRedirect | HttpResponse:
    cd = pre_populate_context_dict(request, {})
    return render(request, 'maio_admin/home.html', cd)
