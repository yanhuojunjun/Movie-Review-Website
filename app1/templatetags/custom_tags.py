from django import template

register = template.Library()


@register.filter(name='range_stars')
def range_stars(value):
    return range(value)
