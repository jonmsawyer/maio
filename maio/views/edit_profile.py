'''
File: dashboard.py

Module: ``maio.views.dashboard``
'''

from __future__ import annotations

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def edit_profile(request: HttpRequest) -> HttpResponse:
    cd = {}
    return render(request, 'maio/edit_profile.html', cd)
