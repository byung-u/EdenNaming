# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _
# from django_summernote.widgets import SummernoteInplaceWidget

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field
from crispy_forms.bootstrap import InlineCheckboxes, InlineRadios

from .models import NamingUserInput, Suri81UserInput
from .choices import (GENDER_CHOICES, ORDER_CHOICES,
                      LASTNAME_CHOICES, LOCATION_CHOICES)

class NamingForm(forms.ModelForm):

    class Meta:
        model = NamingUserInput
        fields = ['gender', 'location', 'last_name', 'birth_date', 'birth_time']
        # fields = ['gender', 'birth_order', 'location', 'last_name', 'birth_date', 'birth_time']
        labels = {
            'gender': _('아이의 성별'),
            # 'birth_order': _('태어난 순서'),
            'location': _('태어난 지역'),
            'last_name': _('사용할 성씨'),
            'birth_date': _('태어난 날짜'),
            'birth_time': _('태어난 시간'),
        }
        widgets = {
                'gender': forms.Select(attrs={
                    'style': 'width:100px; margin-left:100px',
                    }),
                # 'birth_order': forms.Select(attrs={
                # 'style': 'width:100px; margin-left:100px',
                # }),
                'location': forms.Select(attrs={
                    'style': 'width:100px; margin-left:100px',
                    }),
                'last_name': forms.Select(attrs={
                    'style': 'width:100px; margin-left:100px',
                    }),
                'birth_date': forms.TextInput(attrs={
                    'style': 'width:150px; margin-left:100px',
                    'required': True,
                    'type': 'date',
                    }),
                'birth_time': forms.TextInput(attrs={
                    'style': 'width:150px; margin-left:100px',
                    'required': True,
                    'type': 'time',
                    }),
        }

    def __init__(self, *args, **kwargs):
        super(NamingForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit(
            'submit', _('요청하기'), css_class='btn-success',
            style='float:right; clear: right;',
            ))

class Suri81Form(forms.ModelForm):

    class Meta:
        model = Suri81UserInput
        fields = ['name', ]
        labels = {
            'name': _('한글이름'),
        }
        widgets = {
                'name': forms.TextInput(attrs={
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
            'submit', _('제출'), css_class='btn-success', 
            style='float:right; clear: right;',
            ))
