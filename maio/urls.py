"""
 maio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls import include

from maio.admin import admin_site

from maio.views import home
from maio.views import dashboard
from maio.views import logout


urlpatterns = [
    url(r'^admin/?', admin_site.urls),
    #url(r'^portal/?', include(portal.urls, namespace='portal')),
    url(r'^dashboard/?', dashboard, name='dashboard'),
    url(r'^logout/?', logout, name='logout'),
    url(r'^$', home, name='home'),
]
