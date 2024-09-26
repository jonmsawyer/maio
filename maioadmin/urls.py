'''
File: urls.py

Module: ``maio.urls``

Maio URL Configuration
'''

from __future__ import annotations
from typing import Any

from django.urls import path #, include
from django.contrib.auth.decorators import login_required

from maio import views

from maioadmin import views


app_name = 'maioadmin'

urlpatterns: list[Any] = [
    # Views
    path('user/<str:username>/', login_required(views.user_dashboard), name='user_dashboard'),

    # AJAX
    # path('ajax/delete_media/', ajax.delete_media, name='delete_media'),

    # Home
    path('', login_required(views.home), name='home'),
]
