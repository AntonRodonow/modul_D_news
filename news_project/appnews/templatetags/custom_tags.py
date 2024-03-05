from datetime import datetime

from django import template

register = template.Library()


@register.simple_tag(name='ctime')  # отдает объект в котором формат можно указать либо тут в теге, либо в шаблоне
def current_time(format_string='%b %d %Y %I:%M%p'):
    return datetime.now().strftime(format_string)


@register.simple_tag(name='url_for_filter', takes_context=True)
def url_replace(context, **kwargs):  # возварщает оконцовку урла, например author=2&dateStart=&dateFinish=&page=4
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    return d.urlencode()
