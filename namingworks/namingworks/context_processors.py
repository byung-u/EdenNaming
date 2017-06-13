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
                ('pronounce', {'title': _('음령오행')}),
                ('three_type', {'title': _('삼원오행')}),
                ('resource_type', {'title': _('자원오행')}),
                ('suri', {'title': _('수리음양')}),
                ('numeric_sum', {'title': _('원형이정')}),
                ('invalid_hanja', {'title': _('불용한자')}),
                ('saju', {'title': _('주역괘효')}),
            ]),
        }),
        ('service', {
            'title': _('고객센터'),
            'icon': 'question-sign',
            'submenu': OrderedDict([
                ('qna', {'title': _('온라인문의')}),
                ('suri81', {'title': _('이름운세(수리성명)')}),
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
