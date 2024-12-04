from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .commands import ProcessaServicos, EnviaEmail
from django.core import serializers
from django.contrib import messages 
from .models import Servicos
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
            processa_servicos.salva_servico()
            processa_servicos.associa_categorias()

            #TODO falta enviar o email para o status em orçamento de forma automatica, pode fazer isso, nesse local
            # envia_email = EnviaEmail()
            # envia_email.trata_emails(servico_id)

            messages.success(request, "Cliente adicionado com sucesso!")

            return redirect('novo_servico')
        else:
            return HttpResponse(f'ERRO {processa_servicos.erro_msg}')


#TODO Em desenvolvimento 
def editar_servico(request):
    if request.method == 'GET':
        lista_servicos = Servicos.objects.all()
        return render(request, 'editar_servico.html', {'servicos': lista_servicos})

    elif request.method == 'POST':
        id_servico = request.POST.get('servico_id')
        servicos = Servicos.objects.filter(id=id_servico)

        json_formatado = json.loads(serializers.serialize('json', servicos))

        return JsonResponse({'valores': json_formatado})
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








