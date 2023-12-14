'''
File: urls.py

Module: ``maio.urls``

Maio URL Configuration
'''

from __future__ import annotations

from django.urls import path, include

from maio import views
from maio.admin import admin_site


urlpatterns = [
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin_site.urls),
    #path('portal/', include(portal.urls, namespace='portal')),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout, name='logout'),
    path('upload_media/', views.upload_media, name='upload_media'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('search/', views.search, name='search'),
    path('', views.home, name='home'),
]
