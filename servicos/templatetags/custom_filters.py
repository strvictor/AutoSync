# from django import template
# from babel.numbers import format_currency

# register = template.Library()

# @register.filter
# def multiply(qtd, num1):
#     try:
#         multiplicacao = (qtd * num1)
#         return format_currency(multiplicacao, 'BRL', locale='pt_BR')
#     except (TypeError, ValueError):
#         return ''


from django import template
from babel.numbers import format_currency

register = template.Library()

@register.simple_tag
def calcular_total(quantidade, preco, valor_mao_de_obra):
    try:
        preco = float(preco)
        valor_mao_de_obra = float(valor_mao_de_obra)
        quantidade = float(quantidade)
        resultado = (quantidade * preco) + valor_mao_de_obra
        return format_currency(resultado, 'BRL', locale='pt_BR')
    except (ValueError, TypeError):
        return ''
