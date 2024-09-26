'''
File: search.py

Module: ``maio.views.search``
'''

from __future__ import annotations

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from maio.lib import pre_populate_context_dict


def search(request: HttpRequest) -> HttpResponse:
    cd = pre_populate_context_dict(request, {})
    return render(request, 'maio/search.html', cd)
