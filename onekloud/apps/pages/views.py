import hashlib

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.core.mail import EmailMessage
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from apps.pages.forms import SignupForm, ContactForm


def home(request):
    ctx = dict()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            subject = "Registration confirmation for Onekloud CRM"
            support_email = 'support@onekloud.com'

            data = form.cleaned_data
            # Store password hash instead of plain-text.
            password = make_password(data['password'])
            data['password'] = password.replace('pbkdf2_sha256$12000$', '')

            key = '{key}{email}'.format(key=settings.ACTIVATION_KEY,
                                        email=data['email']).encode('utf8')
            data['hash'] = hashlib.md5(key).hexdigest()
            html = mark_safe(
                render_to_string('pages/activation_email.html', data))
            msg = EmailMessage(
                subject, html, support_email, [data['email']],
                headers={'Reply-To': support_email})
            msg.content_subtype = 'html'
            msg.send()
            messages.success(
                request, "Thank you! We have sent you activation link to "
                         "{email}.".format(email=data['email']))
    else:
        ctx['form'] = SignupForm()
    return render(request, 'pages/home.html', ctx)


def pricing(request):
    ctx = dict(title="Pricing")
    return render(request, 'pages/pricing.html', ctx)


def contact(request):
    ctx = dict(title="Contact")
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            html = mark_safe(render_to_string('pages/email.html', data))
            recipients = ('aldash@onekloud.com', 'samantha@onekloud.com')
            msg = EmailMessage(
                data['subject'], html, data['email'], recipients,
                headers={'Reply-To': data['email']})
            msg.content_subtype = 'html'
            msg.send()
            messages.success(
                request, "Thank you for getting in touch! We will reply you "
                         "within 24 hours.")
        else:
            messages.error(request, form.errors)
    else:
        ctx['form'] = ContactForm()
    return render(request, 'pages/contact.html', ctx)


def privacy(request):
    ctx = dict(title="Privacy Statement")
    return render(request, 'pages/privacy.html', ctx)


def terms_of_service(request):
    ctx = dict(title="Terms of Service")
    return render(request, 'pages/terms_of_service.html', ctx)
