from django import template
from babel.numbers import format_currency

register = template.Library()

@register.filter
def multiply(value, arg):

    try:
        multiplicacao = value * arg
        return format_currency(multiplicacao, 'BRL', locale='pt_BR')
    except (TypeError, ValueError):
        return ''
