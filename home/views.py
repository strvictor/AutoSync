from django.shortcuts import render
from servicos.models import Servicos, ServicoCategoriaQuantidade
from babel.numbers import format_currency
from django.db.models import Count, Sum, F, ExpressionWrapper, DecimalField
from django.db.models.functions import TruncMonth

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
        'total_valor_finalizados': format_currency(float(total_valor_finalizados), 'BRL', locale='pt_BR'),
        'valor_medio': format_currency(float(valor_medio), 'BRL', locale='pt_BR'),
        'em_orcamento': em_orcamento.count(),
        'orc_reprovado': orcamento_reprovado.count()
    }

    contexto = {}

    # Obter dados agrupados por mês e categoria
    servicos_por_categoria_mes = (
        ServicoCategoriaQuantidade.objects.filter(servico__status="Finalizado")
        .annotate(mes=TruncMonth('servico__data_finalizacao'))  # Agrupar por mês
        .values('mes', 'categoria__titulo')  # Selecionar mês e categoria
        .annotate(total_servicos=Sum('quantidade'))  # Somar a quantidade de serviços por categoria
        .order_by('mes', 'categoria__titulo')  # Ordenar por mês e por categoria
    )

    # Mapear os meses para abreviações
    meses_abreviados = {
        1: "jan", 2: "fev", 3: "mar", 4: "abr", 5: "mai", 6: "jun",
        7: "jul", 8: "ago", 9: "set", 10: "out", 11: "nov", 12: "dez"
    }

    # Processar os dados em um formato estruturado
    dados_estruturados = {}
    categorias_set = set()
    
    for servico in servicos_por_categoria_mes:
        mes = meses_abreviados[servico['mes'].month]
        categoria = servico['categoria__titulo']
        quantidade = servico['total_servicos']

        categorias_set.add(categoria)

        if mes not in dados_estruturados:
            dados_estruturados[mes] = {}

        if categoria not in dados_estruturados[mes]:
            dados_estruturados[mes][categoria] = 0

        dados_estruturados[mes][categoria] += quantidade

    # Organizar as categorias e preparar os dados finais
    categorias = sorted(categorias_set)
    meses = list(dados_estruturados.keys())
    
    quantidade_servicos_por_mes = {
        mes: [dados_estruturados[mes].get(categoria, 0) for categoria in categorias]
        for mes in meses
    }

    # Preparar dados para os gráficos de vendas e pedidos
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

    orders_month_report = [
        {'mes': servico['mes'].strftime('%Y-%m'), 'total_valor': float(servico['total_valor'])}
        for servico in servicos_por_mes
    ]

    orders_month_report_labels = [item['mes'] for item in orders_month_report]
    orders_month_report_data = [item['total_valor'] for item in orders_month_report]

    nomes_meses = [meses_abreviados[int(data.split('-')[1])] for data in orders_month_report_labels]

    contexto['valores_meses'] = orders_month_report_data
    contexto['nomes_meses'] = nomes_meses
    contexto['dados_cards'] = dados_cards
    contexto['meses_retorno'] = meses
    contexto['categorias'] = categorias
    contexto['quantidade_servicos_por_mes'] = quantidade_servicos_por_mes

    return render(request, 'home.html', contexto)