from django import template
from django.http import HttpResponse

import six

register = template.Library()

CENSOR_LIST = ['дурак',
               'лох',
               'очнехорошийчеловек']


@register.filter(name='censor')
def censor(value: str) -> HttpResponse or str:

    try:
        if isinstance(value, six.string_types):
            value1 = value.split()
            for i in CENSOR_LIST:
                for j in value1:
                    if j.lower() == i:
                        value = value.replace(j, ("*" * len(j)))
            return str(value)
    except (ValueError, TypeError):
        html = f"<html><body>Invalid input.</body></html>"
        return HttpResponse(html)
