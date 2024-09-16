'''
File: dashboard.py

Module: ``maio.views.dashboard``
'''

from __future__ import annotations

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from maio.lib import pre_populate_context_dict

@login_required
def search(request: HttpRequest) -> HttpResponse:
    cd = pre_populate_context_dict(request, {})
    return render(request, 'maio/search.html', cd)
