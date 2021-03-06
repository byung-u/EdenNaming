"""edennaming URL Configuration

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
# from django.contrib.flatpages import views
# from django.contrib.auth.decorators import login_required

from home.views import index, login , login_mailsent, login_req, logout, contact
from naming.views import naming, naming_result, suri81, suri81_result


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^summernote/', include('django_summernote.urls')),
] + [
    # home
    url(r'^$', index, name='index'),

    url(r'^login/$', login, name='login'),
    url(r'^login/mailsent/$', login_mailsent, name='login_mailsent'),
    url(r'^login/req/(?P<token>[a-z0-9\-]+)$', login_req, name='login_req'),
    url(r'^logout/$', logout, name='logout'),

    url(r'^client/contact/$', contact, name='contact'),
] + [
    # service
    url(r'^service/naming/$', naming, name='naming'),
    url(r'^service/naming_result$', naming_result, name='naming_result'),

    url(r'^service/suri81/$', suri81, name='suri81'),
    url(r'^service/suri81_result/$', suri81_result, name='suri81_result'),
]



    # flatpages
    # url(r'^pages/', include('django.contrib.flatpages.urls')),
    # url(r'^(?P<url>.*/)$', views.flatpage, name='flatpage'),
