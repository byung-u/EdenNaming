# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django import forms
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import NamingUserInput, Suri81UserInput

class NamingForm(forms.ModelForm):

    class Meta:
        model = NamingUserInput
        b_date = '태어난 날짜 (예: %s)' % datetime.now().strftime('%Y-%m-%d')
        b_time = '태어난 시간 (예: %s)' % datetime.now().strftime('%H:%M')
        fields = ['gender', 'birth_order', 'location', 'last_name', 'birth_date', 'birth_time']
        labels = {
            'gender': _('아이의 성별'),
            'birth_order': _('태어난 순서'),
            'location': _('태어난 지역'),
            'last_name': _('사용할 성씨'),
            'birth_date': _(b_date),
            'birth_time': _(b_time),
        }
        widgets = {
                'gender': forms.Select(attrs={
                    'style': 'width:100px; margin-left:200px',
                    }),
                'birth_order': forms.Select(attrs={
                    'style': 'width:100px; margin-left:200px',
                    }),
                'location': forms.Select(attrs={
                    'style': 'width:100px; margin-left:200px',
                    }),
                'last_name': forms.Select(attrs={
                    'style': 'width:100px; margin-left:200px',
                    }),
                'birth_date': forms.DateInput(
                    attrs={
                    'style': 'width:150px; margin-left:200px',
                    'type': 'date',
                    }),
                'birth_time': forms.TimeInput(
                    attrs={
                    'style': 'width:150px; margin-left:200px',
                    'type': 'time',
                    }),
        }

    def __init__(self, *args, **kwargs):
        super(NamingForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit(
            'submit', _('결과 요청하기'), css_class='btn-success bsbtn',
            # style='float:center; clear: center;',
            ))


class Suri81Form(forms.ModelForm):

    class Meta:
        model = Suri81UserInput
        fields = ['name', ]
        labels = {
            'name': _('한글 이름'),
        }
        widgets = {
                'name': forms.TextInput(attrs={
                    'placeholder': '한글만 입력해주세요',
                    'style': 'width:150px; margin-left:100px',
                    'required': True,
                    'type': 'text',
                    }),
        }

    def __init__(self, *args, **kwargs):
        super(Suri81Form, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit(
            'submit', _('결과 요청하기'), css_class='btn-success bsbtn',
            # style='float:center; clear: center;',
            ))
