'''
File: urls.py

Module: ``maio.urls``

Maio URL Configuration
'''

from __future__ import annotations
from typing import Any

from django.urls import path, include
from django.contrib.auth.decorators import login_required

from maio import views
from maio.views import ajax
from maio.admin import admin_site


urlpatterns: list[Any] = [
    # Admin
    path('maio_admin/', include('maioadmin.urls', namespace='maio_admin')),
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('password/', login_required(views.PasswordChangeView.as_view()), name='password'),
    path('password_change_done/', login_required(views.PasswordChangeDoneView.as_view()), name='password_change_done'),
    path('admin/', admin_site.urls),

    # Maio Views
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout, name='logout'),
    path('upload_media/', login_required(views.UploadMediaView.as_view()), name='upload_media'),
    path('edit_profile/', login_required(views.edit_profile), name='edit_profile'),
    path('search/', login_required(views.search), name='search'),

    # AJAX
    path('ajax/delete_media/', login_required(ajax.delete_media), name='delete_media'),
    path('ajax/change_thumbnail/', login_required(ajax.change_thumbnail), name='change_thumbnail'),
    path('', views.home, name='home'),
]
