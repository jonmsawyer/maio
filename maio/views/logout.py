'''
File: logout.py

Module: ``maio.views.logout``
'''

from __future__ import annotations

from django.shortcuts import redirect
from django.contrib.auth import logout as django_logout
from django.http import HttpRequest, HttpResponseRedirect, HttpResponsePermanentRedirect


def logout(request: HttpRequest) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
    django_logout(request)
    return redirect('home')
