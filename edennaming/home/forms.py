# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
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
        self.helper.layout = Layout(
                Field('email', css_class='input-small'),
                FormActions(
                    Submit('submit', '로그인', css_class="btn-success"),
                )
        )
        self.fields['email'].widget.attrs['style'] = 'width:100%; margin-bottom:15px;'


    def clean(self):
        cleaned_data = super(EmailLoginForm, self).clean()
        return cleaned_data


class EmailSendForm(forms.Form):
    email = forms.EmailField(
            max_length=255,
            widget=forms.TextInput(attrs={
                'class': 'form-control',
            })
        )
    content = forms.CharField(
                widget=forms.Textarea(),
            )

    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-sm-2'
    helper.field_class = 'col-sm-8'
    helper.layout = Layout(
            Field('email', css_class='input-small'),
            Field('content', css_class='input-small'),
            FormActions(
                Submit('send_email', '전 송', css_class="btn-success"),
            )
    )

    def __init__(self, *args, **kwargs):
        super(EmailSendForm, self).__init__(*args, **kwargs)
        self.fields['email'].label = '<span class="glyphicon glyphicon-envelope"></span> E-mail 주소:'
        self.fields['email'].widget.attrs['style'] = 'width:90%;'
        self.fields['content'].label = '<span class="glyphicon glyphicon-pencil"></span> 내용'
        self.fields['content'].widget.attrs['style'] = 'width:90%;'

    def validate(self, value):
        super(EmailSendForm, self).validate(value)
        for email in value:
            validate_email(email)
