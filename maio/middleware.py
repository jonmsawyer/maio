'''
File: middleware.py

Module: ``maio.middleware``

Maio's Middleware.
'''

from __future__ import annotations
from typing import Any, Callable

from django.http import HttpRequest, HttpResponse

from maio.models import FileStat, UserSetting, MaioUser

class FileStatMiddleware:
    '''Inject the FileStat data into the request.'''
    get_response: Callable[..., Any]

    def __init__(self, get_response: Callable[..., Any]) -> None:
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request: HttpRequest) -> HttpResponse:
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        setattr(
            request,
            'file_stat',
            FileStat.objects.latest('date_modified'),
        )

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

class UserSettingMiddleware:
    get_response: Callable[..., Any]

    def __init__(self, get_response: Callable[..., Any]) -> None:
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request: HttpRequest) -> HttpResponse:
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        try:
            user_setting, user_setting_created = UserSetting.objects.get_or_create(user=MaioUser.objects.get(user=request.user))
            if user_setting_created:
                user_setting.save()
            user_setting.previous_page = request.META.get('HTTP_REFERER' , '/') # type: ignore;
            user_setting.save()
        except TypeError:
            user_setting = UserSetting()
        setattr(request, 'user_setting', user_setting)

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
