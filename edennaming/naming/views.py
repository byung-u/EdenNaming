# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re

from django.utils.translation import ugettext as _
from django.shortcuts import render
from django.views.decorators.cache import never_cache

# from .forms import NamingForm, Suri81Form, Suri81ResultForm
from .forms import NamingForm, Suri81Form
from .naming import get_new_korean_name, get_hanja_name, get_your_luck


def naming(request):

    form = NamingForm()

    if request.method == 'POST':
        form = NamingForm(request.POST)

        names = None
        if form.is_valid():
            print(request.user)
#            if user_limit_check(request.user) is False:
#                return render(request, 'naming_limit.html', {
#                    'title': _('작명정보입력'),
#                    'names': names,
#                    'flag': flag,
#                })

            location = form.cleaned_data['location']
            last_name = form.cleaned_data['last_name']
            gender = form.cleaned_data['gender']
            # birth_order = form.cleaned_data['birth_order']
            # msg = '내부서버 에러입니다. E-mail 문의 부탁드립니다. %s %s' % (birth_date, birth_time)
            birth_date = form.cleaned_data['birth_date']
            birth_time = form.cleaned_data['birth_time']
            birth_datetime = '%s %s' % (birth_date, birth_time)
            names, flag = get_new_korean_name(gender, location, last_name, birth_datetime)

        if names is None:  # error
            return render(request, 'home/error.html', {
                'title': _('작명정보입력'),
                'msg': '내부서버 에러입니다. E-mail 문의 부탁드립니다.',
            })

        return render(request, 'naming/naming_result.html', {
            'title': _('작명정보입력'),
            'names': names,
            'flag': flag,
        })
    else:
        return render(request, 'naming/naming_input.html', {
            'title': _('작명정보입력'),
            'form': form,
        })


def naming_result(request):
    return render(request, 'naming/naming_result.html', {
        'title': _('작명결과'),
    })


def input_name_check(input_name):
    # TODO : 2, 4, 5 이름
    if 5 < len(input_name) < 1:
        return False, '현재 2~4글자 한글이름만 지원합니다. (%s)' % input_name

    if len(set(input_name)) == 1:
        err_msg = '입력하신 모든 글자가 같습니다. (%s)' % input_name
        return False, err_msg

    r = re.compile('[A-z0-9]')
    ret = r.search(input_name)
    if ret is not None:
        err_msg = '영어나 숫자는 처리 불가합니다. (%s)' % input_name
        return False, err_msg

    return True, None


def suri81(request):
    form = Suri81Form()

    if request.method == 'POST':
        form = Suri81Form(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            ret, error_msg = input_name_check(name)
            if ret is False:
                return render(request, 'naming/suri81_input.html', {
                    'title': _('이름 운세'),
                    'form': form,
                    'flag': False,
                    'error_msg': error_msg,
                })
            hanja1, hanja2, hanja3 = get_hanja_name(name)
            if hanja1 is None:
                return render(request, 'naming/suri81_input.html', {
                    'title': _('이름 운세'),
                    'form': form,
                    'flag': False,
                    'error_msg': '4글자 입력하는 경우 (2자 성씨 + 2자 이름)만 지원하고 있습니다.',
                })

            return render(request, 'naming/suri81_trying.html', {
                'name': name,
                'hanja1': hanja1,
                'hanja2': hanja2,
                'hanja3': hanja3,
            })

    return render(request, 'naming/suri81_input.html', {
        'title': _('이름 운세'),
        'form': form,
        'flag': True,
        'error_msg': '',
    })


@never_cache
def suri81_result(request):

    if request.method == 'GET':
        # form = Suri81ResultForm(request.GET)
        input_name = request.GET.get('input_name')
        print('---------')
        print(input_name)
        print('---------')

        ret, err_msg = input_name_check(input_name)
        if ret is None:
            return render(request, 'naming/suri81_result.html', {
                'result': err_msg,
            })

        hanja1 = request.GET.get('hanja1')
        hanja2 = request.GET.get('hanja2')
        hanja3 = request.GET.get('hanja3')
        # print(hanja1, hanja2, hanja3)
        your_luck = get_your_luck(input_name, hanja1, hanja2, hanja3)
        if your_luck is None:
            print(input_name, hanja1, hanja2, hanja3)
            return render(request, 'naming/suri81_result.html', {
                'result': '내부 서버 에러입니다.',
            })

        return render(request, 'naming/suri81_result.html', {
            'result': your_luck,
        })

    return render(request, 'home/index.html', {
        'title': _('미래작명당'),
    })
