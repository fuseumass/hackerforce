from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def order_by(context, arg):
    return order_by_custom(context, "order_by", arg)

@register.simple_tag(takes_context=True)
def order_by_custom(context, get_name, arg):
    existing_arg = context.request.GET.get(get_name)
    existing = '?' + context.request.GET.urlencode()
    existing = existing.replace(f'&{get_name}={existing_arg}', '')
    existing = existing.replace(f'?{get_name}={existing_arg}', '')
    order_by_arg = f"-{arg}" if existing_arg == arg else arg
    if order_by_arg[:2] == "--":
        order_by_arg = order_by_arg[2:]
    if not existing.startswith('?'):
        existing = '?' + existing
    return f"{existing}&{get_name}={order_by_arg}"