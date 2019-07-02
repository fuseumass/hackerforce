from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def order_by(context, arg):
    return order_by_custom(context, "order_by", arg)

@register.simple_tag(takes_context=True)
def order_by_custom(context, get_name, arg):
    q = context.request.GET.get("q") or ""
    order_by = f"-{arg}" if context.request.GET.get(get_name) == arg else arg
    return f"?q={q}&{get_name}={order_by}"