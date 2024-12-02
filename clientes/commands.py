from .models import Cliente, Carro
from django.core import serializers
import re, json
from django.shortcuts import get_object_or_404


class ProcessaUsuarios:
    def __init__(self, requisicao, id_usuario=False):
        self.id_usuario = id_usuario
        self.erro_msg = None
        if self.id_usuario:
            body = json.loads(requisicao.body)
    
            self.nome = body['nome']
            self.sobrenome = body['sobrenome']
            self.email = body['email']
            self.cpf = body['cpf']

        else:
            self.requisicao_post = requisicao.POST
            self.nome = self.requisicao_post.get('nome')
            self.sobrenome = self.requisicao_post.get('sobrenome')
            self.email = self.requisicao_post.get('email')
            self.cpf = self.requisicao_post.get('cpf')

            self.carros = self.requisicao_post.getlist('carro')
            self.placas = self.requisicao_post.getlist('placa')
            self.anos = self.requisicao_post.getlist('ano')
    
    
    def valida_dados(self):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        cpf_regex_pontos = r'^\d{3}\.\d{3}\.\d{3}\-\d{2}$'
        cpf_regex_sem_pontos = r'^\d{3}\.?\d{3}\.?\d{3}\-?\d{2}$'
        
        if not re.match(cpf_regex_pontos, self.cpf) and not re.match(cpf_regex_sem_pontos, self.cpf):
            self.erro_msg = 'CPF inválido, reveja o formato.'
            return False
        
        if Cliente.objects.filter(cpf=self.cpf).exclude(id=self.id_usuario).exists():
            self.erro_msg = 'CPF já cadastrado.'
            return False
        
        if not re.match(email_regex, self.email):
            self.erro_msg = 'E-mail inválido, reveja o formato.'
            return False
        
        if Cliente.objects.filter(email=self.email).exclude(id=self.id_usuario).exists():
            self.erro_msg = 'E-mail já cadastrado.'
            return False
        
        cpf_clean = str(self.cpf).replace('.', '').replace('-', '')

        # Verificar se o CPF limpo tem 11 dígitos
        if not cpf_clean.isnumeric() or len(cpf_clean) != 11:
            self.erro_msg = 'CPF inválido, deve conter apenas 11 dígitos numéricos.'
            return False
        
        # CPF válido, armazena o CPF limpo
        self.cpf = cpf_clean

        return True
    
    
    def salva_cliente(self):
        self.cliente_bd = Cliente(
            nome=self.nome,
            sobrenome=self.sobrenome,
            email=self.email,
            cpf=self.cpf
        )
        self.cliente_bd.save()


    def atualiza_cliente(self):
        self.cliente_bd = get_object_or_404(Cliente, id=self.id_usuario)
        self.cliente_bd.nome = self.nome
        self.cliente_bd.sobrenome = self.sobrenome
        self.cliente_bd.email = self.email
        self.cliente_bd.cpf = self.cpf
        self.cliente_bd.save()
    

    def salva_carro(self):
        relaciona_carros = list(zip(self.carros, self.placas, self.anos))
        for nome_carro, placa, ano in relaciona_carros:

            carro = Carro(
                carro=nome_carro,
                placa=placa,
                ano=ano,
                cliente=self.cliente_bd
            )
            if Carro.objects.filter(placa=placa).exists():
                self.erro_msg = f'Placa {placa} ja existe no banco de dados. O carro {nome_carro} ano {ano} não foi cadastrado.'
                return False
            
            carro.save()


class AtualizaUsuarios:
    def __init__(self, requisicao):
        self.erro_msg = None
        self.requisicao_post = requisicao.POST
        self.id_cliente = self.requisicao_post.get('id_cliente')

        self.id_cliente_bd = Cliente.objects.filter(id=self.id_cliente)
        self.carros_cliente = Carro.objects.filter(cliente=self.id_cliente_bd[0])


    def valida_usuario(self):
        if self.id_cliente_bd.exists():
            return True
        else:
            self.erro_msg = 'não encontrei esse usuário!'
            return False


    def serializa_query(self, queryset, indice=False):
        # Serializa o queryset para JSON
        json_formatado = json.loads(serializers.serialize('json', queryset))
        
        if indice:
            json_retorno = json_formatado[0]['fields']
        else:
            json_retorno = [{'fields': carro['fields'], 'id': carro['pk']} for carro in json_formatado]
        
        return json_retorno
        

class AtualizaCarros:
    def __init__(self, requisicao, id_carro):
        self.erro_msg = None
        self.id_carro = id_carro
        self.requisicao_post = requisicao.POST

        self.nome_carro = self.requisicao_post.get('carro')
        self.placa_carro = self.requisicao_post.get('placa')
        self.ano_carro = self.requisicao_post.get('ano')

        self.carro_bd = None

        try:
            self.carro_bd = Carro.objects.get(id=self.id_carro)
        except Carro.DoesNotExist:
            self.erro_msg = f'id {self.id_carro} <carro> não encontrado.'


    def valida_carro(self):

        if not self.carro_bd:
            return False

        if Carro.objects.filter(placa=self.placa_carro).exclude(id=self.id_carro).exists():
            self.erro_msg = f'Placa {self.placa_carro} já existente.'
            return False

        return True


    def atualiza_carro(self):
        # Atualiza os atributos do carro e salva no banco
        self.carro_bd.carro = self.nome_carro
        self.carro_bd.placa = self.placa_carro
        self.carro_bd.ano = self.ano_carro
        self.carro_bd.save()
