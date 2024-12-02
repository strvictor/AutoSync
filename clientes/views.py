from django.shortcuts import render, redirect
from .models import Cliente
from .commands import ProcessaUsuarios, AtualizaUsuarios, AtualizaCarros
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages


def clientes(request):
    if request.method == 'GET':
        clientes_bd = Cliente.objects.all()
        return render(request, 'clientes.html', {'clientes': clientes_bd})
    
    elif request.method == 'POST':
        processa_post = ProcessaUsuarios(request)
        if processa_post.valida_dados():
            processa_post.salva_cliente()
            salva_carros = processa_post.salva_carro()
            if salva_carros == False:
                messages.info(request, processa_post.erro_msg)
                return redirect('clientes')
            
            messages.success(request, "Cliente adicionado com sucesso!")
            return redirect('clientes')
        else:
            print(processa_post.erro_msg)
            return render(request, 'clientes.html', {'erro': processa_post.erro_msg})
    
    else:
        return render(request, 'clientes.html')


def atualiza_cliente(request):
    if request.method == 'GET':
        return redirect('clientes')
        
    elif request.method == 'POST':
        atualiza_usuarios = AtualizaUsuarios(request)
        if atualiza_usuarios.valida_usuario():

            # Pega o JSON formatado conforme o parâmetro passado
            json_clientes = atualiza_usuarios.serializa_query(atualiza_usuarios.id_cliente_bd, indice=True)
            json_carros = atualiza_usuarios.serializa_query(atualiza_usuarios.carros_cliente)
            
            dados = {'cliente': json_clientes,
                     'carros': json_carros}
            
            return JsonResponse(dados)
        else:
            messages.success(request, atualiza_usuarios.erro_msg)
            return redirect('clientes.html')
        
    else:
        return render(request, 'clientes.html')


@csrf_exempt
def atualiza_carro(request, id_carro):
    if request.method == 'GET':
        return redirect('clientes')
        
    elif request.method == 'POST':
        atualiza_carros_bd = AtualizaCarros(request, id_carro)
        if atualiza_carros_bd.valida_carro():
            atualiza_carros_bd.atualiza_carro()
            messages.success(request, 'Carro atualizado com sucesso!')
            return redirect('clientes')
        else:
            messages.error(request, atualiza_carros_bd.erro_msg)
            return redirect('clientes.html')
         
    else:
        return render(request, 'clientes.html')
    

def update_cliente(request, id_cliente):
    if request.method == 'GET':
        return redirect('clientes')
    
    elif request.method == 'POST':
        atualiza_cliente = ProcessaUsuarios(request, id_cliente)
        if atualiza_cliente.valida_dados():
            atualiza_cliente.atualiza_cliente()

            messages.success(request, 'Cliente atualizado com sucesso!')
            return redirect('clientes')
        else:
            messages.error(request, atualiza_cliente.erro_msg)
            return redirect('clientes.html')
         
    
    else:
        return render(request, 'clientes.html')