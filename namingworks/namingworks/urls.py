"""namingworks URL Configuration

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
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.flatpages import views

from .views import index
from home.views import login, login_mailsent, login_req, logout, profile
from naming.views import naming, naming_result

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^summernote/', include('django_summernote.urls')),
    url(r'^$', index, name='index'),

    url(r'^login/$', login, name='login'),
    url(r'^login/mailsent/$', login_mailsent, name='login_mailsent'),
    url(r'^login/req/(?P<token>[a-z0-9\-]+)$', login_req, name='login_req'),
    url(r'^logout/$', logout, name='logout'),

    url(r'^profile/$', profile, name='profile'),

    url(r'^naming/$', naming, name='naming'),
    url(r'^naming/naming_result$', naming_result, name='naming_result'),

    # flatpages
    url(r'^pages/', include('django.contrib.flatpages.urls')),
    url(r'^(?P<url>.*/)$', views.flatpage, name='flatpage'),
]
