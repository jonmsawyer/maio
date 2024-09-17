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
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin_site.urls),
    #path('portal/', include(portal.urls, namespace='portal')),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout, name='logout'),
    path('upload_media/', login_required(views.UploadMediaView.as_view()), name='upload_media'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('search/', views.search, name='search'),

    # Maio Admin
    path('maio_admin/', views.maio_admin.home, name='maio_admin'),

    # AJAX
    path('ajax/delete_media/', ajax.delete_media, name='delete_media'),
    path('', views.home, name='home'),
]
