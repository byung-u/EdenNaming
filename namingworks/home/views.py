# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import login as user_login, logout as user_logout
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect, reverse
from django.template import Context
from django.template.loader import get_template
from django.utils.translation import ugettext as _
from django.views.decorators.cache import never_cache

from datetime import datetime, timedelta

from .models import EmailToken
from .forms import EmailLoginForm, EmailSendForm
from .helper import sendEmailToken


def login(request):
    if request.user.is_authenticated():
        return redirect('profile')

    form = EmailLoginForm()

    if request.method == 'POST':
        form = EmailLoginForm(request.POST)
        if form.is_valid():
            # Remove previous tokens
            email = form.cleaned_data['email']
            EmailToken.objects.filter(email=email).delete()

            # Create new
            token = EmailToken(email=email)
            token.save()

            sendEmailToken(request, token)
            return redirect(reverse('login_mailsent'))

    return render(request, 'login.html', {
        'form': form,
        'title': _('Login'),
    })


@never_cache
def login_req(request, token):
    time_threshold = datetime.now() - timedelta(hours=1)
    try:
        token = EmailToken.objects.get(token=token,
                                       created__gte=time_threshold)
    except ObjectDoesNotExist:
        print('[ERR] Invalid token', token)
        return render(request, 'login_notvalidtoken.html', {
            'title': _('유효하지 않은 토큰')}
        )

    email = token.email
    try:
        user = User.objects.get(email=email)
    except ObjectDoesNotExist:
        user = User.objects.create_user(email, email, token)
        user.save()

    token.delete()

    # Set backend manually
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    user_login(request, user)

    contexts = {
        'index': True,
    }
    return render(request, 'index.html', contexts)


@never_cache
def login_mailsent(request):
    return render(request, 'login_mailsent.html', {
        'title': _('EMail 전송'),
    })


def logout(request):
    user_logout(request)
    return redirect(reverse('index'))


def profile(request):
    return redirect(reverse('index'))


def contact(request):
    form_class = EmailSendForm()

    if request.method == 'POST':
        form = form_class(data=request.POST)

        if form.is_valid():
            contact_name = request.POST.get(
                'contact_name'
            , '')
            contact_email = request.POST.get(
                'contact_email'
            , '')
            form_content = request.POST.get('content', '')

            # Email the profile with the contact information
            template = get_template('contact_template.html')
            context = Context({
                'contact_name': contact_name,
                'contact_email': contact_email,
                'form_content': form_content,
            })
            content = template.render(context)

            email = EmailMessage(
                "New contact form submission",
                content,
                "Your website" +'',
                ['youremail@gmail.com'],
                headers = {'Reply-To': contact_email }
            )
            email.send()
            return redirect('contact')

    return render(request, 'contact.html', {
        'form': form_class,
    })

