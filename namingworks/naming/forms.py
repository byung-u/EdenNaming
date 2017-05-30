# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _
from django_summernote.widgets import SummernoteInplaceWidget

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import NamingUserInput
from .choices import (GENDER_CHOICES, ORDER_CHOICES,
                      LASTNAME_CHOICES, LOCATION_CHOICES)

class NamingForm(forms.ModelForm):

    class Meta:
        model = NamingUserInput
        fields = ['gender', 'birth_order', 'location', 'last_name', 'birth_datetime']
        labels = {
            'gender': _('아이의 성별'),
            'birth_order': _('태어난 순서'),
            'location': _('태어난 지역'),
            'last_name': _('사용할 성씨'),
            'birth_datetime': _('태어난 시각'),
        }
        widgets = {
            'desc': SummernoteInplaceWidget(),
        }

    def __init__(self, *args, **kwargs):
        super(NamingForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', _('제출')))



