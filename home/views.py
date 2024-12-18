from django.shortcuts import render
from django.http import HttpResponse
from servicos.models import Servicos


from django.db.models import Sum, F, ExpressionWrapper, DecimalField
from django.db.models.functions import TruncMonth
from django.shortcuts import render
from django.contrib import messages
from servicos.models import Servicos


def home(request):
    # Filtrar serviços por status
    em_orcamento = Servicos.objects.filter(status='Em Orçamento')
    orcamento_reprovado = Servicos.objects.filter(status='Orçamento Reprovado')
    pendentes = Servicos.objects.filter(status='Em Andamento')
    finalizados = Servicos.objects.filter(status='Finalizado')

    # Calcular totais
    total_pendentes = pendentes.count()
    total_valor_pendentes = sum(
        item.categoria.preco * item.quantidade
        for servico in pendentes
        for item in servico.servicocategoriaquantidade_set.all()
    )

    total_finalizados = finalizados.count()
    total_valor_finalizados = sum(
        item.categoria.preco * item.quantidade
        for servico in finalizados
        for item in servico.servicocategoriaquantidade_set.all()
    )

    try:
        valor_medio = total_valor_finalizados / total_finalizados
    except ZeroDivisionError:
        valor_medio = 0
    
    dados_cards = {
        'total_pendentes': total_pendentes,
        'total_valor_pendentes': total_valor_pendentes,
        'total_finalizados': total_finalizados,
        'total_valor_finalizados': total_valor_finalizados,
        'valor_medio': valor_medio,
        'em_orcamento': em_orcamento.count(),
        'orc_reprovado': orcamento_reprovado.count()

    }

    contexto = {}

    # Gerar relatório de serviços finalizados agrupados por mês
    servicos_por_mes = (
        Servicos.objects.filter(status="Finalizado")
        .annotate(mes=TruncMonth('data_finalizacao'))  # Agrupar por mês
        .annotate(
            valor_total=ExpressionWrapper(
                F('servicocategoriaquantidade__quantidade') * F('servicocategoriaquantidade__categoria__preco'),
                output_field=DecimalField(max_digits=10, decimal_places=2)
            )
        )
        .values('mes')
        .annotate(total_valor=Sum('valor_total'))  # Soma total por mês
        .order_by('mes')
    )

    # Preparar dados para o gráfico
    orders_month_report = [
        {'mes': servico['mes'].strftime('%Y-%m'), 'total_valor': float(servico['total_valor'])}
        for servico in servicos_por_mes
    ]
    orders_month_report_labels = [item['mes'] for item in orders_month_report]
    orders_month_report_data = [item['total_valor'] for item in orders_month_report]

    meses_abreviados = {
    "01": "jan",
    "02": "fev",
    "03": "mar",
    "04": "abr",
    "05": "mai",
    "06": "jun",
    "07": "jul",
    "08": "ago",
    "09": "set",
    "10": "out",
    "11": "nov",
    "12": "dez",
    }

    nomes_meses = [meses_abreviados[data.split('-')[1]] for data in orders_month_report_labels]

    contexto['valores_meses'] = orders_month_report_data
    contexto['nomes_meses'] = nomes_meses
    contexto['dados_cards'] = dados_cards

    print(contexto)

    return render(request, 'home.html', contexto)
