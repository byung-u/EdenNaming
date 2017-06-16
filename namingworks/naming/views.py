# -*- coding: utf-8 -*-
from __future__ import unicode_literals

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
            birth_date = form.cleaned_data['birth_date']
            birth_time = form.cleaned_data['birth_time']

            birth_datetime = '%s %s' % (birth_date, birth_time)
            names, flag = get_new_korean_name(gender, location, last_name, birth_datetime)

        return render(request, 'naming_result.html', {
            'title': _('작명정보입력'),
            'names': names,
            'flag': flag,
        })
    else:
        return render(request, 'naming_input.html', {
            'title': _('작명정보입력'),
            'form': form,
        })


def naming_result(request):
    return render(request, 'naming_result.html', {
        'title': _('작명결과'),
    })


def suri81(request):
    form = Suri81Form()

    if request.method == 'POST':
        form = Suri81Form(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            hanja1, hanja2, hanja3 = get_hanja_name(name)

        return render(request, 'suri81_trying.html', {
            'name': name,
            'hanja1': hanja1,
            'hanja2': hanja2,
            'hanja3': hanja3,
        })

    return render(request, 'suri81_input.html', {
        'title': _('이름 운세'),
        'form': form,
    })


@never_cache
def suri81_result(request):

    if request.method == 'GET':
        # form = Suri81ResultForm(request.GET)
        input_name = request.GET.get('input_name')
        print('---------')
        print(input_name)
        print('---------')
        hanja1 = request.GET.get('hanja1')
        hanja2 = request.GET.get('hanja2')
        hanja3 = request.GET.get('hanja3')
        # print(hanja1, hanja2, hanja3)
        your_luck = get_your_luck(input_name, hanja1, hanja2, hanja3)

        return render(request, 'suri81_result.html', {
            'result': your_luck,
        })

    return render(request, 'index.html', {
        'title': _('미래작명당'),
    })
