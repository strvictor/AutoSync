from django.shortcuts import render
from django.http import HttpResponse
from servicos.models import Servicos

def home(request):
    # Filtrar serviços por status
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
        contexto = {
            'total_pendentes': total_pendentes,
            'total_valor_pendentes': total_valor_pendentes,
            'total_finalizados': total_finalizados,
            'total_valor_finalizados': total_valor_finalizados,
            'valor_medio': total_valor_finalizados / total_finalizados,
        }
    except ZeroDivisionError:
        contexto = {
            'total_pendentes': total_pendentes,
            'total_valor_pendentes': total_valor_pendentes,
            'total_finalizados': total_finalizados,
            'total_valor_finalizados': total_valor_finalizados,
            'valor_medio': '0',
        }
    
    return render(request, 'home.html', contexto)
