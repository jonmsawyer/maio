'''
File: dashboard.py

Module: ``maio.views.dashboard``
'''

from __future__ import annotations
from typing import Any

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
# from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserChangeForm

from maio.lib import pre_populate_context_dict

from maio.forms import UserSettingForm, UserChangeForm

def _user_profile(request: HttpRequest, context: dict[str, Any]) -> HttpResponse | HttpResponseRedirect:
    '''User Change'''
    action = context.get('action')
    if request.method == 'POST' and action == 'user_profile':
        user_profile_form = UserChangeForm(request.POST, instance=request.user, request=request)
    else:
        user_profile_form = UserChangeForm(instance=request.user, request=request)

    context['user_profile_saved'] = False
    context['user_profile_form'] = user_profile_form

    if user_profile_form.is_valid():
        if request.method == 'POST':
            if action == 'user_profile':
                user_profile_form.save()
                context['user_profile_saved'] = True
    return user_profile_form

def _user_setting(request: HttpRequest, context: dict[str, Any]) -> HttpResponse | HttpResponseRedirect:
    '''User Change'''
    action = context.get('action')
    if request.method == 'POST' and action == 'user_setting':
        user_settings_form = UserSettingForm(request.POST, instance=request.user_setting)
    else:
        user_settings_form = UserSettingForm(initial=request.user_setting.__dict__)

    context['user_settings_saved'] = False
    context['user_settings_form'] = user_settings_form

    if user_settings_form.is_valid():
        if request.method == 'POST':
            if action == 'user_setting':
                user_settings_form.save()
                context['user_settings_saved'] = True
    return user_settings_form

def edit_profile(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    cd = pre_populate_context_dict(request, {})
    cd['action'] = request.POST.get('action')
    _user_profile_form = _user_profile(request, cd)
    _user_settings_form = _user_setting(request, cd)
    if request.method == 'POST':
        if cd['user_profile_saved'] or cd['user_settings_saved']:
            if request.user_setting.redirect_to_previous_page_after_setting_save:
                return HttpResponseRedirect(request.user_setting.previous_page)

    return render(request, 'maio/edit_profile.html', cd)
