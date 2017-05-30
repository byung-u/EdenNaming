
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string


def sendEmailToken(request, token):
    html = render_to_string('mail/token_html.html', {'token': token}, request)
    text = render_to_string('mail/token_text.html', {'token': token}, request)

    msg = EmailMultiAlternatives(
            settings.EMAIL_LOGIN_TITLE,
            text,
            settings.EMAIL_SENDER,
            [token.email])
    msg.attach_alternative(html, 'text/html')
    msg.send(fail_silently=False)
