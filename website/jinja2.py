from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse

from jinja2 import Environment

# from widget_tweaks import render_field, add_class, set_attr
import widget_tweaks


def environment(**options):
    env = Environment(**options)
    env.globals.update(
        {
            "static": staticfiles_storage.url,
            "url": reverse,
            "render_field": widget_tweaks.templatetags.widget_tweaks.render_field,
        }
    )
    env.filters.update(
        {
            "add_class": widget_tweaks.templatetags.widget_tweaks.add_class,
            "set_attr": widget_tweaks.templatetags.widget_tweaks.set_attr,
        }
    )
    return env
