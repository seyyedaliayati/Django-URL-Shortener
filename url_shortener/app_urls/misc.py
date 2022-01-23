import string

from hashids import Hashids
from django.urls import reverse
from django.utils.timezone import datetime

from .models import Click

HASH_SALT = 'VyIZlWoq7VQCvJmq54gVHz5mb7GbaXdcT3Qz8dRssMyaYpTZl2ONBBnDA788Ef'
ALPHABET = string.ascii_lowercase

hashids = Hashids(salt=HASH_SALT, alphabet=ALPHABET)


def hash_encode(num):
    """
    Returns hashids.encode(num) with salt.
    """
    return hashids.encode(num)


def get_absolute_short_url(request, alias, remove_schema=True):
    """
    Returns absolute redirect URL, given the `request` object
    and the `alias`.
    Set `remove_schema` to False to prevent schema
    from being removed (default: True).
    """
    if alias:
        full_url = request.build_absolute_uri(
            reverse('app_urls:alias', args=(alias,)))
    else:
        full_url = request.build_absolute_uri(reverse('app_urls:index'))
    if remove_schema:
        return full_url[len(request.scheme)+3:]
    return full_url

def get_client_ip(request):
    """
    Returns request's ip address.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def process_new_click(request, link):
    """
    Gets or creates a click object and increases its `clicks_count`.
    """
    today = datetime.today()
    click, _ = Click.objects.get_or_create(
        link=link,
        clicked_date=today,
        ip_address=get_client_ip(request)
    )
    click.clicks_count += 1
    click.save()
    return click
