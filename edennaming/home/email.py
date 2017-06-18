# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.mail import get_connection, EmailMultiAlternatives
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


def sendEmailContact(request, from_addr, content):
    connection = get_connection()
    connection.open()

    html = render_to_string('mail/contact_template.html', 
            {'from_addr': from_addr, 'content': content, }, request)
    text = render_to_string('mail/contact_template.html', {'content': content}, request)
    print(from_addr)

    msg = EmailMultiAlternatives(
            "문의 메일",
            text,
            from_addr,
            ['iam.byungwoo@gmail.com',],
            )
    msg.attach_alternative(html, 'text/html')
    msg.send(fail_silently=False)
    connection.close()
