# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field
from crispy_forms.bootstrap import FormActions


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
    email = forms.EmailField(
            max_length=255,
            label='',
            widget=forms.TextInput(attrs={
                'class': 'form-control',
            })
        )
    content = forms.CharField(
                widget=forms.Textarea(),
            )

    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.layout = Layout(
            Field('email', css_class='input-xlarge'),
            Field('content', rows="5", css_class='input-xlarge'),
            FormActions(
                Submit('send_email', 'Send Email',
                    style='float:right; clear: right;',
                    css_class="btn-success"),
            )
    )

    def __init__(self, *args, **kwargs):
        super(EmailSendForm, self).__init__(*args, **kwargs)
        self.fields['email'].label = "E-mail 주소:"
        self.fields['content'].label = "내용:"

    def validate(self, value):
        super(EmailSendForm, self).validate(value)
        for email in value:
            validate_email(email)
