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
            birth_order = form.cleaned_data['birth_order']
            birth_datetime = form.cleaned_data['birth_datetime']

            get_new_korean_name(gender, birth_order,
                                location, last_name, birth_datetime)

        return render(request, 'naming_result.html', {
            'form': form,
            'title': _('NamingResult'),
        })
    else:
        return render(request, 'naming_input_again.html', {
            'form': form,
            'title': _('NamingInput'),
        })


def naming_result(request):
    return render(request, 'naming_result.html', {
        'title': _('NamingResult'),
    })
