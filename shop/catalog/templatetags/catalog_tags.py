from django import template

register = template.Library()


@register.filter
def multiply(value, arg):
    return value * arg


@register.filter
def toman(value):
    if value is None:
        return '0'
    return '{:,}'.format(value)
