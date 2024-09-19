'''
File: home.py

Module: ``maio.views.home``
'''

from __future__ import annotations

from django.shortcuts import render
from django.shortcuts import redirect

from django.http import (
    HttpRequest, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect,
)
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User

from maio.forms import LoginForm
from maio.lib import pre_populate_context_dict


def home(
    request: HttpRequest
) -> HttpResponseRedirect | HttpResponsePermanentRedirect | HttpResponse:
    cd = pre_populate_context_dict(request, {})
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username', '')
            password = form.cleaned_data.get('password', '')
            try:
                findUser = User._default_manager.get(username__iexact=username)
            except User.DoesNotExist:
                findUser = None
            if findUser is not None:
                username = findUser.username
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        if request.user.is_authenticated:
            return redirect('dashboard')
        form = LoginForm()
    cd['form'] = form
    return render(request, 'maio/home.html', cd)

