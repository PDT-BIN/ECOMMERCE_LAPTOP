# GENERATE TOKEN.
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six
# from django.utils import six
# ENCODE DATA.
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
# SEND MAIL.
from django.http import HttpRequest
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth.models import AbstractBaseUser


class ActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user: AbstractBaseUser, timestamp: int) -> str:
        return f'{six.text_type(user.pk)} {six.text_type(timestamp)} {six.text_type(int(user.is_active))}'

    def send_email(self, request: HttpRequest, user: AbstractBaseUser, subject: str,  template: str) -> None:
        data = {
            'domain': get_current_site(request).domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': self.make_token(user),
        }
        message = render_to_string(template_name=template, context=data)
        EmailMessage(subject, message, from_email=None, to=[user.email]).send()


ACCOUNT_ACTIATION_TOKEN = ActivationTokenGenerator()
