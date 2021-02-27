from django import template
import ast

register = template.Library()

@register.simple_tag()
def multiplication(value, arg, *args, **kwargs):
    return value * arg


@register.filter
def in_category(things, category):
    return things.filter(category=category)

@register.simple_tag()
def division(value, arg, *args, **kwargs):
    return value / arg
