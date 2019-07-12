from django import template
import urllib

register = template.Library()


@register.simple_tag(takes_context=True)
def modify_get(context, arg_name, arg_value):
    get = dict(context.request.GET)
    if arg_name in get:
        del get[arg_name]
    existing = urllib.parse.urlencode(get)
    if existing:
        existing = existing + '&'
    return f"?{existing}{arg_name}={arg_value}"