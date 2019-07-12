from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def order_by(context, arg):
    return order_by_custom(context, "order_by", arg)

@register.simple_tag(takes_context=True)
def order_by_custom(context, get_name, arg):
    existing_arg = context.request.GET.get(get_name)
    existing = context.request.GET.urlencode()
    existing = existing.replace(f'&{get_name}={existing_arg}', '')
    order_by = f"-{arg}" if existing_arg == arg else arg
    if order_by[:2] == "--":
        order_by = order_by[2:]
    return f"?{existing}&{get_name}={order_by}"