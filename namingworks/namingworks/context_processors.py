# -*- coding: utf-8 -*-
from collections import OrderedDict

from django.conf import settings
from django.contrib.flatpages.models import FlatPage
from django.utils.translation import ugettext_lazy as _


def default(request):
    # title = None
    # remove i18n_patterns prefix for flatpage
    url = request.path
    # url = request.path.replace('/' + request.LANGUAGE_CODE, '')
    if settings.FORCE_SCRIPT_NAME:
        url = url[len(settings.FORCE_SCRIPT_NAME):]
    base_content = FlatPage.objects.filter(url=url).first()

    # submenu = None
    menu = OrderedDict([
        ('about', {
            'title': _('이용안내'),
            'icon': 'pencil',
            'submenu': OrderedDict([
                ('naming', {'title': _('미래작명당 소개')}),
            ]),
        }),
        ('naming', {
            'title': _('성명학'),
            'icon': 'book',
            'submenu': OrderedDict([
                ('theory', {'title': _('성명학 이론')}),
                ('rules', {'title': _('작명법의 종류')}),
                ('destiny', {'title': _('사주구성 및 보충오행')}),
                ('pillars', {'title': _('수리와 오행')}),
            ]),
        }),
        ('client', {
            'title': _('고객센터'),
            'icon': 'question-sign',
            'submenu': OrderedDict([
                ('contact', {'title': _('온라인문의')}),
            ]),
        }),
    ])

    rp = request.path[len(settings.FORCE_SCRIPT_NAME):]

    for k, v in menu.items():
        path = '/{}/'.format(k)

        if rp.startswith(path):
            v['active'] = True
            # title = v['title']

            # if 'submenu' in v:
            #     submenu = v['submenu']

            #     for sk, sv in v['submenu'].items():
            #         sv['path'] = '{}{}/'.format(path, sk)
            #         subpath = sv['path']

            #         if rp == subpath:
            #             sv['active'] = True
            #             # title = sv['title']

    c = {
        'menu': menu,
        'base_content': base_content.content if base_content else '',
    }
    return c
