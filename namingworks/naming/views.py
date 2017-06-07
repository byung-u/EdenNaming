# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext as _
from django.shortcuts import render

from .forms import NamingForm
from .naming import get_new_korean_name


def naming(request):

    form = NamingForm()

    if request.method == 'POST':
        form = NamingForm(request.POST)
        if form.is_valid():
            location = form.cleaned_data['location']
            last_name = form.cleaned_data['last_name']
            gender = form.cleaned_data['gender']
            # birth_order = form.cleaned_data['birth_order']
            birth_date = form.cleaned_data['birth_date']
            birth_time = form.cleaned_data['birth_time']

            birth_datetime = '%s %s' % (birth_date, birth_time)
            names = get_new_korean_name(gender, location, last_name, birth_datetime)
            print(names)

        return render(request, 'naming_result.html', {
            'names': names,
        })
    else:
        return render(request, 'naming_input.html', {
            'form': form,
            'title': _('NamingInput'),
        })


def naming_result(request):
    return render(request, 'naming_result.html', {
        'title': _('NamingResult'),
    })
