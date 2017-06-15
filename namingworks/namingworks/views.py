# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.utils.translation import ugettext as _


def index(request):
    return render(request, 'index.html', {
        'title': _('이든작명연구소'),
        'index': True,
    })
