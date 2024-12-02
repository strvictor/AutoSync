from django import template
import locale

register = template.Library()

@register.filter
def multiply(value, arg):

    try:
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        multiplicacao = value * arg
        return locale.currency(multiplicacao, grouping=True, symbol=False)
    except (TypeError, ValueError):
        return ''
