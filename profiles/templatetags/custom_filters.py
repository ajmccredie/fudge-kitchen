from django import template

register = template.Library()

@register.filter(name='get_attr')
def get_attr(obj, attr, default=None):
    return getattr(obj, attr, default)
