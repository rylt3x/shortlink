from core import models
import random
import string
import requests
import validators

from django.urls import path
from .forms import SourceLinkForm


def record_url(source_link, forward_link, session_key=None):
    source_link_form = SourceLinkForm({'source_link': source_link,
                                       'forward_link': forward_link,
                                       'session': session_key})
    if source_link_form.is_valid():
        source_link_form.save()


def generate_random_string(size=7, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def validate_url(url: str):
    is_valid = validators.url(url)
    if is_valid:
        return True
    return False


def create_short_link(source_link, session_key=None) -> tuple:
    url = source_link

    if not validate_url(url):
        return 'null', 'error'

    while True:
        generated_slug = generate_random_string()
        if not models.SourceLink.objects.filter(source_link=generated_slug).exists():
            record_url(generated_slug, url, session_key)
            return generated_slug, 'created'
