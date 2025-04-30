# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Estoque, CategoriaManutencao
from decimal import Decimal, InvalidOperation
from .models import Estoque, Reabastecimento
from django.contrib import messages
from django.db.models import F


def estoque(request):
    if request.method == "GET":
        estoque = Estoque.objects.filter(empresa=request.empresa)
        qtd_itens = len(estoque)
        qtd_minima = Estoque.objects.filter(empresa=request.empresa, quantidade_em_estoque__lt=F('quantidade_minima')).count()
        ultima_atualizacao = Estoque.objects.filter(empresa=request.empresa).order_by('-atualizado_em').first().atualizado_em.strftime("%d/%m/%Y %H:%M") if Estoque.objects.filter(empresa=request.empresa).exists() else None
        
        return render(request, "estoque.html", {"qtd_itens": qtd_itens, 'qtd_minima': qtd_minima, 'ultima_atualizacao': ultima_atualizacao})


def reabastecer_estoque(request):
    if request.method == "POST":
        item_id = request.POST.get("item")
        quantidade = int(request.POST.get("quantidade"))

        item = get_object_or_404(Estoque, id=item_id, empresa=request.empresa)

        # cria histórico e atualiza estoque
        Reabastecimento.objects.create(item=item, quantidade_adicionada=quantidade, empresa=request.empresa)
        item.quantidade_em_estoque += quantidade
        item.save()

        messages.success(request, f"{quantidade} unidades adicionadas ao estoque do item {item.nome.titulo}.")
        return redirect("reabastecer_estoque")
    
   # Obtém o item_id da query string (se existir)
    item_id = request.GET.get("id")
    item_nome = None
    item_quantidade = None

    if item_id:
        item = get_object_or_404(Estoque, id=item_id, empresa=request.empresa)
        item_nome = item.nome
        item_quantidade = item.quantidade_em_estoque

    estoque = Estoque.objects.filter(empresa=request.empresa).select_related('nome').all()

    return render(request, "reabastecer.html", {
        "estoque": estoque,
        "item_id": item_id,
        "item_nome": item_nome,
        "item_quantidade": item_quantidade,
    })


def quantidade_minima(request):
    if request.method == "GET":

        estoque = Estoque.objects.filter(empresa=request.empresa, quantidade_em_estoque__lt=F('quantidade_minima'))
        for c in estoque:
            print(f'{c.nome}, {c.quantidade_em_estoque}')
        return render(request, "quantidade_minima.html", {"estoque": estoque})
    
    
def ultimos_reabastecimentos(request):
    if request.method == "GET":
        reabastecimentos = Reabastecimento.objects.filter(empresa=request.empresa)
        return render(request, "ultimos_reabastecimentos.html", {"reabastecimentos": reabastecimentos})
    

def criar_item_estoque(request):
    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        preco = request.POST.get('preco')
        estoque_atual = request.POST.get('estoque_atual')
        estoque_minimo = request.POST.get('estoque_minimo')

        # Validação dos campos obrigatórios
        if not nome or not preco or not estoque_atual or not estoque_minimo:
            messages.error(request, "Todos os campos são obrigatórios.")
            return redirect('reabastecer_estoque')

        try:
            preco = Decimal(preco)
            estoque_atual = int(estoque_atual)
            estoque_minimo = int(estoque_minimo)

            if preco < 0 or estoque_atual < 0 or estoque_minimo < 0:
                messages.error(request, "Valores não podem ser negativos.")
                return redirect('reabastecer_estoque')

            # Criação da categoria e item no estoque
            categoria, _ = CategoriaManutencao.objects.get_or_create(
                empresa=request.empresa,
                titulo=nome,
                defaults={'preco': preco}
            )

            # Atualiza o preço se já existia e mudou
            if categoria.preco != preco:
                categoria.preco = preco
                categoria.save()

            Estoque.objects.create(
                empresa=request.empresa,
                nome=categoria,
                quantidade_em_estoque=estoque_atual,
                quantidade_minima=estoque_minimo
            )

            messages.success(request, f"Item '{categoria.titulo}' adicionado com sucesso!")
            return redirect('reabastecer_estoque')

        except (ValueError, InvalidOperation):
            messages.error(request, "Preencha os campos com valores válidos.")
            return redirect('reabastecer_estoque')

    return redirect('reabastecer_estoque')