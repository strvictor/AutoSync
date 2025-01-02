from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .commands import ProcessaServicos, EnviaEmail
from django.core import serializers
from django.contrib import messages 
from .models import Servicos, Cliente, Carro
import json


#TODO Falta validar as mensagens de retorno ao front-end
def novo_servico(request):
    if request.method == 'GET':
        clientes_obj, categorias_obj = ProcessaServicos(request).retorna_obj()
        return render(request, 'novo_servico.html', {
            'clientes': clientes_obj,
            'categorias': categorias_obj
        })

    elif request.method == 'POST':
        processa_servicos = ProcessaServicos(request)
        if processa_servicos.valida_ids():
            protocolo = processa_servicos.salva_servico()
            processa_servicos.associa_categorias()

            messages.success(request, "Serviço adicionado com sucesso!")

            return redirect('servico', protocolo)
        else:
            return HttpResponse(f'ERRO {processa_servicos.erro_msg}')


#TODO Em desenvolvimento 
def editar_servico(request):
    if request.method == 'GET':
        lista_servicos = Servicos.objects.all()
        return render(request, 'editar_servico.html', {'servicos': lista_servicos})

    elif request.method == 'POST':
        id_servico = request.POST.get('servico_id')
        servicos = Servicos.objects.filter(id=id_servico).select_related('cliente', 'carro').prefetch_related('categoria_manutencao')
        
        if servicos.exists():
            servico = servicos.first()
            cliente = servico.cliente
            carro = servico.carro
            categorias = servico.categoria_manutencao.all()

            servico_data = {
                'id': servico.id,
                'titulo': servico.titulo,
                'cliente': {
                    'id': cliente.id,
                    'nome': cliente.nome,
                    'sobrenome': cliente.sobrenome,
                    'email': cliente.email,
                    'cpf': cliente.cpf,
                },
                'carro': {
                    'id': carro.id,
                    'carro': carro.carro,
                    'placa': carro.placa,
                    'ano': carro.ano,
                },
                'categorias': [{'id': categoria.id, 'titulo': categoria.titulo, 'preco': categoria.preco} for categoria in categorias],
                'data_inicio': servico.data_inicio,
                'data_entrega': servico.data_entrega,
            }

            return JsonResponse({'valores': servico_data})
        else:
            return JsonResponse({'error': 'Serviço não encontrado'}, status=404)
    else:
        return redirect('editar_servico')

def listar_servico(request):
    if request.method == 'GET':
        servicos = Servicos.objects.all()
        return render(request, 'lista_servico.html', {'servicos': servicos})
    else:
        return redirect('listar_servico')


def protocolo(request, protocolo):
    if request.method == 'GET':
        servicos = get_object_or_404(Servicos, protocolo=protocolo)
        return render(request, 'servico.html', {'servico': servicos})
    else:
        return redirect('listar_servico')


def alterar_servico(request, servico_id):
    if request.method == 'POST':
        processa_servico = ProcessaServicos(request)
        protocolo = processa_servico.muda_status_servico(servico_id)

        messages.success(request, "Serviço atualizado com sucesso!")

        print('Envia Email com Celery')
        envia_email = EnviaEmail()
        envia_email.trata_emails(servico_id)
        
        return redirect('servico', protocolo) 

    return redirect('listar_servico') 


def carros_por_cliente(request, cliente_id):
    processa_servicos = ProcessaServicos(request)
    
    return processa_servicos.busca_carros_por_cliente(cliente_id)








