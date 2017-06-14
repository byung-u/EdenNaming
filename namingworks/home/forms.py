# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class EmailLoginForm(forms.Form):
    email = forms.EmailField(
            max_length=255,
            label='',
            widget=forms.TextInput(attrs={
                'placeholder': 'E-mail 주소',
                'class': 'form-control',
            })
        )

    def __init__(self, *args, **kwargs):
        super(EmailLoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', _('로그인')))

    def clean(self):
        cleaned_data = super(EmailLoginForm, self).clean()
        return cleaned_data

class EmailSendForm(forms.Form):
    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    content = forms.CharField(
            required=True,
            widget=forms.Textarea
            )

    def __init__(self, *args, **kwargs):
        super(EmailSendForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = "Your name:"
        self.fields['email'].label = "Your email:"
        self.fields['content'].label = "What do you want to say?"
