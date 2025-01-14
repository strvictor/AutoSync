from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .commands import ProcessaServicos, EnviaEmail
from django.contrib import messages 
from .models import Servicos, CategoriaManutencao


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
            validacao_estoque = processa_servicos.processa_estoque()

            if validacao_estoque:
                protocolo = processa_servicos.salva_servico()
                processa_servicos.associa_categorias()

            else:
                messages.error(request, processa_servicos.erro_msg)
                return render(request, 'novo_servico.html')
            
            if processa_servicos.erro_msg:
                messages.error(request, processa_servicos.erro_msg)
            else:
                messages.success(request, "Serviço adicionado com sucesso!")
            return redirect('servico', protocolo)
        else:
            return HttpResponse(f'ERRO {processa_servicos.erro_msg}')


def editar_servico(request):
    if request.method == 'GET':
        lista_servicos = Servicos.objects.all()
        return render(request, 'editar_servico.html', {'dados': {'servicos': lista_servicos}})

    elif request.method == 'POST':
        servico_id = request.POST.get('servico_id')
        protocolo = request.POST.get('protocolo')
        titulo_servico = request.POST.get('servico')
        mecanico = request.POST.get('mecanico')

        categorias = request.POST.getlist('categorias')
        valor_mao_de_obra = request.POST.getlist('valor_mao_de_obra')
        quantidade = request.POST.getlist('quantidades')

        data_inicio = request.POST.get('data_inicio')
        data_entrega = request.POST.get('data_entrega')

        validacao, servico_editado = ProcessaServicos.edita_servico(servico_id, titulo_servico, mecanico, categorias, valor_mao_de_obra, quantidade, data_inicio, data_entrega)

        if not validacao:
            messages.error(request, servico_editado)
            return render(request, 'editar_servico.html') 
        else:
            if servico_editado:
                messages.error(request, servico_editado)
                return redirect('servico', protocolo)
            else:
                messages.success(request, "Serviço modificado com sucesso!")
            return redirect('servico', protocolo)
    
    else:
        return redirect('editar_servico')

def seleciona_servico(request):
    if request.method == 'GET':
        return redirect('novo_servico')
    else:
        servico_id = request.POST.get('servico_selecionado')
        servico = get_object_or_404(Servicos, id=servico_id)
        
        dados = {
            'id': servico_id,
            'protocolo': servico.protocolo,
            'titulo': servico.titulo,
            'nome': servico.cliente.nome,
            'sobrenome': servico.cliente.sobrenome,
            'carro': servico.carro.carro,
            'placa': servico.carro.placa,
            'categoria': servico.categoria_manutencao.all(),
            'relacao': servico.servicocategoriaquantidade_set.all(),
            'categorias_existentes': CategoriaManutencao.objects.all(),
            'servicos': Servicos.objects.all(),
            'mecanico_responsavel': servico.mecanico_resp,
            'data_inicio': servico.data_inicio,
            'data_entrega': servico.data_entrega,
        }
            
        return render(request, 'editar_servico.html', {'dados': dados})


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

        envia_email = EnviaEmail()
        envia_email.trata_emails(servico_id)
        
        return redirect('servico', protocolo) 

    return redirect('listar_servico') 


def carros_por_cliente(request, cliente_id):
    processa_servicos = ProcessaServicos(request)
    
    return processa_servicos.busca_carros_por_cliente(cliente_id)


