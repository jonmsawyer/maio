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
            setattr(
                request,
                'user_setting',
                UserSetting.objects.filter(user=MaioUser.objects.get(user=request.user)) \
                    .latest('date_added'),
            )
        except TypeError:
            setattr(
                request,
                'user_setting',
                UserSetting.objects.none(),
            )

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
