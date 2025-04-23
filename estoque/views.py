# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Estoque, Reabastecimento
from django.contrib import messages


def estoque(request):
    qtd_itens = Estoque.objects.all().count()
    print(estoque)
    return render(request, "estoque.html", {"qtd_itens": qtd_itens})


def reabastecer_estoque(request):
    if request.method == "POST":
        item_id = request.POST.get("item")
        quantidade = int(request.POST.get("quantidade"))

        item = get_object_or_404(Estoque, id=item_id)

        # cria histórico e atualiza estoque
        Reabastecimento.objects.create(item=item, quantidade_adicionada=quantidade)
        item.quantidade_em_estoque += quantidade
        item.save()

        messages.success(request, f"{quantidade} unidades adicionadas ao estoque de {item.nome.titulo}.")
        return redirect("reabastecer_estoque")

    estoque = Estoque.objects.select_related('nome').all()
    return render(request, "reabastecer.html", {"estoque": estoque})
