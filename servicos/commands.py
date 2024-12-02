from servicos.models import Servicos, CategoriaManutencao
from django.shortcuts import get_object_or_404
from clientes.models import Cliente, Carro
from django.http import JsonResponse
from servicos.tasks import valida_info_email


class ProcessaServicos:
    def __init__(self, requisicao):
        self.erro_msg = None
        self.requisicao_post = requisicao.POST

        self.cliente_selecionado = self.requisicao_post.get('cliente')
        self.carro_selecionado = self.requisicao_post.get('carro')
        self.titulo_servico = self.requisicao_post.get('titulo_servico')
        self.mecanico_responsavel = self.requisicao_post.get('mecanico_responsavel')
        self.notifica_cliente = self.requisicao_post.get('notificar')
        self.categorias_servico = self.requisicao_post.getlist('categorias')
        self.quantidades_servico = self.requisicao_post.getlist('quantidades')
        self.data_inicio = self.requisicao_post.get('data_inicio')
        self.data_entrega = self.requisicao_post.get('data_entrega')

        self.status = self.requisicao_post.get('status')  
        self.avisa_cliente = self.requisicao_post.get('notifica_cliente') == 'on'  


    def valida_ids(self):
        # Valida o cliente
        try:
            self.cliente_obj = Cliente.objects.get(id=self.cliente_selecionado)
        except Cliente.DoesNotExist:
            self.erro_msg = 'Id do cliente não encontrado!'
            return False

        # Valida o carro
        try:
            self.carro_obj = Carro.objects.get(id=self.carro_selecionado)
        except Carro.DoesNotExist:
            self.erro_msg = 'Id do carro não encontrado!'
            return False

        # Valida categorias e quantidades
        if not self.categorias_servico or not self.quantidades_servico:
            self.erro_msg = 'Categorias e/ou quantidades não fornecidas!'
            return False

        if len(self.categorias_servico) != len(self.quantidades_servico):
            self.erro_msg = 'A quantidade de categorias não corresponde à quantidade de quantidades!'
            return False

        return True


    def associa_categorias(self):
        # Associa as categorias de manutenção (ManyToMany)
        categorias_objs = CategoriaManutencao.objects.filter(id__in=self.categorias_servico)

        # Associa categoria e quantidade (exemplo fictício de ManyToMany com dados extras)
        for categoria_id, quantidade in zip(self.categorias_servico, self.quantidades_servico):
            categoria_obj = categorias_objs.get(id=categoria_id)
            self.salva_servico_bd.categoria_manutencao.add(
                categoria_obj,
                through_defaults={'quantidade': quantidade}  # Exemplo de uso do campo adicional
            )

        self.salva_servico_bd.save()


    def salva_servico(self):
        self.salva_servico_bd = Servicos(
            titulo=self.titulo_servico,
            cliente=self.cliente_obj,
            carro=self.carro_obj,
            data_inicio=self.data_inicio,
            data_entrega=self.data_entrega,
            notifica_cliente=self.notifica_cliente,
            mecanico_resp=self.mecanico_responsavel,
        )
        self.salva_servico_bd.save()


    def retorna_obj(self):
        self.clientes_bd = Cliente.objects.all()
        self.categorias_bd = CategoriaManutencao.objects.all()

        return self.clientes_bd, self.categorias_bd
    
    
    def busca_carros_por_cliente(self, cliente_id):

        carros = Carro.objects.filter(cliente_id=cliente_id)  # Filtra os carros do cliente

        carros_data = [{"id": carro.id, "nome": carro.carro} for carro in carros]  # Formata para JSON
        return JsonResponse({"carros": carros_data})
    
    
    def muda_status_servico(self, servico_id):
        servico = get_object_or_404(Servicos, id=servico_id)

        servico.finalizado = (self.status == 'finalizado')  # Converte o status
        servico.notifica_cliente = self.avisa_cliente  # Atualiza a notificação

        servico.save()
        return servico.protocolo


class EnviaEmail:
    @staticmethod
    def _(id_servico):
        servico_cliente = Servicos.objects.get(id=id_servico)

        if servico_cliente.finalizado:
            # servico finalizado
            valida_info_email.delay(servico_cliente.id)
        else:
            # serviço como pendente ou outro status
            ...