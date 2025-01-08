from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .commands import ProcessaServicos, EnviaEmail
from django.core import serializers
from django.contrib import messages 
from .models import Servicos, CategoriaManutencao
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
# Idéia:
# Adicionar um form para o input de busca de serviço, ao selecionar é enviado o id desse serviço para um endpoint ex: servicos/alterar_serviço<id>
# Pego esse id aqui na view e faço as buscas do serviço, cliente, carro e categorias vinculados, retorno esses dados em contexto para o front end, no formato {json}
# No front end, ao receber esses dados, preencho os campos do form que será habilitado com o evento que foi disparado quando enviei o formulario no step acima, nesse form terá um botão de submit para alterar as categorias e quantidades do serviço:
# Ainda em avaliação se permito mudar o cliente ou só as categorias. 1 - Adicionar uma nova categoria, editar a existente ou remover alguma, da pra usar o mesmo layout que usei ao cadastrar as categorias no front end, na parte de novo serviço.
def editar_servico(request):
    if request.method == 'GET':
        lista_servicos = Servicos.objects.all()
        return render(request, 'editar_servico.html', {'dados': {'servicos': lista_servicos}})

    elif request.method == 'POST':
        servico_id = request.POST.get('servico_id')
        titulo_servico = request.POST.get('servico')
        mecanico = request.POST.get('mecanico')

        categorias = request.POST.getlist('categorias')
        valor_mao_de_obra = request.POST.getlist('valor_mao_de_obra')
        quantidade = request.POST.getlist('quantidades')

        data_inicio = request.POST.get('data_inicio')
        data_entrega = request.POST.get('data_entrega')

        ProcessaServicos.edita_servico(servico_id, titulo_servico, mecanico, categorias, valor_mao_de_obra, quantidade, data_inicio, data_entrega)

        return HttpResponse('Serviço alterado com sucesso!')
    
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


def seleciona_servico(request):
    if request.method == 'GET':
        return redirect('novo_servico')
    else:
        servico_id = request.POST.get('servico_selecionado')

        servicos = Servicos.objects.all()
        categorias_existentes = CategoriaManutencao.objects.all()
        
        servico = Servicos.objects.get(id=servico_id)
        dados = {
            'id': servico_id,
            'titulo': servico.titulo,
            'nome': servico.cliente.nome,
            'sobrenome': servico.cliente.sobrenome,
            'carro': servico.carro.carro,
            'placa': servico.carro.placa,
            'categoria': servico.categoria_manutencao.all(),
            'relacao': servico.servicocategoriaquantidade_set.all(),
            'categorias_existentes': categorias_existentes,
            'servicos': servicos,
            'mecanico_responsavel': servico.mecanico_resp,
            'data_inicio': servico.data_inicio,
            'data_entrega': servico.data_entrega,
        }
            
        return render(request, 'editar_servico.html', {'dados': dados,
                                                  })



