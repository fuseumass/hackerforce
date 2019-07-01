from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def order_by(context, arg):
    q = context.request.GET.get("q") or ""
    order_by = f"-{arg}" if context.request.GET.get("order_by") == arg else arg
    return f"?q={q}&order_by={order_by}"