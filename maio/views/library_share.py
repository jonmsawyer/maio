'''
File: library_share.py

Module: ``maio.views.library_share``
'''

from __future__ import annotations
from typing import Optional

from django.shortcuts import render
# from django.shortcuts import redirect
from django.db.models import Q
from django.contrib.auth.models import User

from django.http import (
    HttpRequest, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect,
    Http404,
)
# from django.contrib.auth import authenticate
# from django.contrib.auth import login

# from maio.forms import LoginForm
from maio.lib import pre_populate_context_dict
from maio.models.choices import PermissionChoices
from maio.models import LibraryShare, MaioUser
from maio.views import dashboard

def library_share(
    request: HttpRequest,
    username: Optional[str] = None
) -> HttpResponseRedirect | HttpResponsePermanentRedirect | HttpResponse:
    cd = pre_populate_context_dict(request, {})
    maio_user = MaioUser.objects.get(user=request.user)
    shares = LibraryShare.objects.filter(~Q(permission=PermissionChoices.DENIED), to_user=maio_user)

    if username:
        for share in shares:
            if share.from_user.user.username == username:
                return dashboard(request, with_username=username)

    cd['shares'] = shares
    cd['js_debug'] = 'true'
    return render(request, 'maio/library_share.html', cd)
