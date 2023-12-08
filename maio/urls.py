'''
File: urls.py

Module: ``maio.urls``

Maio URL Configuration
'''

from django.urls import path
from django.urls import include

from maio.admin import admin_site

from maio.views import home
from maio.views import dashboard
from maio.views import logout


urlpatterns = [
    path('admin/', admin_site.urls),
    #path('portal/', include(portal.urls, namespace='portal')),
    path('dashboard/', dashboard, name='dashboard'),
    path('logout/', logout, name='logout'),
    path('', home, name='home'),
]
