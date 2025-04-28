# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Estoque, Reabastecimento
from django.contrib import messages
from django.db.models import F


def estoque(request):
    if request.method == "GET":
        estoque = Estoque.objects.all()
        qtd_itens = len(estoque)
        qtd_minima = Estoque.objects.filter(quantidade_em_estoque__lt=F('quantidade_minima')).count()
        ultima_atualizacao = Estoque.objects.order_by('-atualizado_em').first().atualizado_em.strftime("%d/%m/%Y %H:%M") if Estoque.objects.exists() else None
        
        return render(request, "estoque.html", {"qtd_itens": qtd_itens, 'qtd_minima': qtd_minima, 'ultima_atualizacao': ultima_atualizacao})


def reabastecer_estoque(request):
    if request.method == "POST":
        item_id = request.POST.get("item")
        quantidade = int(request.POST.get("quantidade"))

        item = get_object_or_404(Estoque, id=item_id)

        # cria histórico e atualiza estoque
        Reabastecimento.objects.create(item=item, quantidade_adicionada=quantidade)
        item.quantidade_em_estoque += quantidade
        item.save()

        messages.success(request, f"{quantidade} unidades adicionadas ao estoque do item {item.nome.titulo}.")
        return redirect("reabastecer_estoque")
    
   # Obtém o item_id da query string (se existir)
    item_id = request.GET.get("id")
    item_nome = None
    item_quantidade = None

    if item_id:
        item = get_object_or_404(Estoque, id=item_id)
        item_nome = item.nome
        item_quantidade = item.quantidade_em_estoque

    estoque = Estoque.objects.select_related('nome').all()

    return render(request, "reabastecer.html", {
        "estoque": estoque,
        "item_id": item_id,
        "item_nome": item_nome,
        "item_quantidade": item_quantidade,
    })


def quantidade_minima(request):
    if request.method == "GET":

        estoque = Estoque.objects.filter(quantidade_em_estoque__lt=F('quantidade_minima'))
        for c in estoque:
            print(f'{c.nome}, {c.quantidade_em_estoque}')
        return render(request, "quantidade_minima.html", {"estoque": estoque})
    
    
def ultimos_reabastecimentos(request):
    if request.method == "GET":
        reabastecimentos = Reabastecimento.objects.all()
        return render(request, "ultimos_reabastecimentos.html", {"reabastecimentos": reabastecimentos})