from django import template
import ast

register = template.Library()

@register.filter # register the template filter with django
def ProductParsingInAdminPanel(value):
    dataset = ast.literal_eval(value)
    return dataset.items()


@register.filter # register the template filter with django
def get_string_as_list(value): # Only one argument.
    return ast.literal_eval(value)


@register.filter # register the template filter with django
def convertDoubleQuotesToSingleQuotes(value): # Only one argument.
    return str(value).replace('"', "'")