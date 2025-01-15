from servicos.models import Servicos, CategoriaManutencao, ServicoCategoriaQuantidade
from django.shortcuts import get_object_or_404
from clientes.models import Cliente, Carro
from django.http import JsonResponse
from servicos.tasks import valida_info_email
from django.db import transaction
from django.conf import settings
from estoque.commands import ProcessaEstoque

class ProcessaServicos:
    def __init__(self, requisicao):
        self.erro_msg = []
        self.requisicao_post = requisicao.POST

        self.cliente_selecionado = self.requisicao_post.get('cliente')
        self.carro_selecionado = self.requisicao_post.get('carro')
        self.titulo_servico = self.requisicao_post.get('titulo_servico')
        self.mecanico_responsavel = self.requisicao_post.get('mecanico_responsavel')
        self.notifica_cliente = self.requisicao_post.get('notificar')
        self.categorias_servico = self.requisicao_post.getlist('categorias')
        self.quantidades_servico = self.requisicao_post.getlist('quantidades')
        self.valor_mao_de_obra = self.requisicao_post.getlist('valor_mao_de_obra')
        self.data_inicio = self.requisicao_post.get('data_inicio')
        self.data_entrega = self.requisicao_post.get('data_entrega')

        self.status = self.requisicao_post.get('status')  
        self.avisa_cliente = self.requisicao_post.get('notifica_cliente') == 'on' #converte o valor do checkbox para True ou False

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
        if not self.categorias_servico or not self.quantidades_servico or not self.valor_mao_de_obra:
            self.erro_msg = 'Categorias, valor de mão de obra e/ou quantidades não fornecidas!'
            return False

        if len(self.categorias_servico) != len(self.quantidades_servico):
            self.erro_msg = 'A quantidade de categorias não corresponde à quantidade de quantidades!'
            return False

        return True

    def valida_estoque(self):
        categorias_objs = CategoriaManutencao.objects.filter(id__in=self.categorias_servico)
        qtd_servicos_estoque_invalido = 0

        for categoria_id, quantidade, _ in zip(self.categorias_servico, self.quantidades_servico, self.valor_mao_de_obra):
            categoria_obj = categorias_objs.get(id=categoria_id)

            estoque = ProcessaEstoque(categoria_obj, quantidade)
            quantidade_minima_em_estoque = estoque.valida_qtd_minima()

            if not quantidade_minima_em_estoque:
                self.erro_msg.append(estoque.erro_msg)
                qtd_servicos_estoque_invalido += 1

        if len(self.categorias_servico) == qtd_servicos_estoque_invalido:
            return False
        return True

    def processa_estoque(self):
        categorias_objs = CategoriaManutencao.objects.filter(id__in=self.categorias_servico)

        for categoria_id, quantidade, _ in zip(self.categorias_servico, self.quantidades_servico, self.valor_mao_de_obra):
            categoria_obj = categorias_objs.get(id=categoria_id)

            estoque = ProcessaEstoque(categoria_obj, quantidade)
            nome_categoria_atual = ServicoCategoriaQuantidade.objects.filter(servico=self.salva_servico_bd, categoria=categoria_obj).first()

            quantidade_salva = nome_categoria_atual.quantidade if nome_categoria_atual else 0
            if estoque.valida_qtd_minima():
                estoque.valida_se_add_ou_acres(quantidade_salva)

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
        return self.salva_servico_bd

    def associa_categorias(self, servico):
        # Associa as categorias de manutenção (ManyToMany)
        categorias_objs = CategoriaManutencao.objects.filter(id__in=self.categorias_servico)

        # Associa categoria e quantidade (exemplo fictício de ManyToMany com dados extras)
        for categoria_id, quantidade, valor_mao_de_obra in zip(self.categorias_servico, self.quantidades_servico, self.valor_mao_de_obra):
            if not valor_mao_de_obra:
                valor_mao_de_obra = 0
            categoria_obj = categorias_objs.get(id=categoria_id)

            estoque = ProcessaEstoque(categoria_obj, quantidade)
            quantidade_minima_em_estoque = estoque.valida_qtd_minima()

            if quantidade_minima_em_estoque:         
                servico.categoria_manutencao.add(
                    categoria_obj,
                    through_defaults={'quantidade': quantidade,
                                    'valor_mao_de_obra': valor_mao_de_obra}
                )

        servico.save()

    @staticmethod
    def edita_servico(servico_id, titulo_servico, mecanico, categorias, valor_mao_de_obra, quantidade, data_inicio, data_entrega):
        erro_msg = []
        qtd_servicos_estoque_invalido = 0
        servico = get_object_or_404(Servicos, id=servico_id)
        categorias_objs = CategoriaManutencao.objects.filter(id__in=categorias)

        # Atualiza os campos básicos do serviço
        servico.titulo = titulo_servico
        servico.mecanico_resp = mecanico
        servico.data_inicio = data_inicio
        servico.data_entrega = data_entrega
        servico.save()

        with transaction.atomic():
            # Itera pelas categorias para criar ou atualizar o modelo intermediário
            for categoria_id, quantidade_, valor_mao_de_obra_ in zip(categorias, quantidade, valor_mao_de_obra):
                if not valor_mao_de_obra_:
                    valor_mao_de_obra_ = 0
                else:
                    valor_mao_de_obra_ = str(valor_mao_de_obra_).replace(',', '.')
                categoria_obj = categorias_objs.get(id=categoria_id)
                
                estoque = ProcessaEstoque(categoria_obj, quantidade_)
                quantidade_minima_em_estoque = estoque.valida_qtd_minima()

                if quantidade_minima_em_estoque:
                    nome_categoria_atual = ServicoCategoriaQuantidade.objects.filter(servico=servico, categoria=categoria_obj).first()

                    quantidade_salva = nome_categoria_atual.quantidade if nome_categoria_atual else 0

                    estoque.valida_se_add_ou_acres(quantidade_salva)

                    # Atualiza ou cria o registro no modelo intermediário
                    servico.categoria_manutencao.through.objects.update_or_create(
                        servico=servico,  # Campo que referencia o serviço
                        categoria=categoria_obj,  # Campo que referencia a categoria
                        defaults={
                            'quantidade': quantidade_,
                            'valor_mao_de_obra': valor_mao_de_obra_,
                        }
                    )
                else:
                    qtd_servicos_estoque_invalido +=1
                    erro_msg.append(estoque.erro_msg)

            # Remove as relações que não estão na lista atual
            servico.categoria_manutencao.through.objects.filter(
                servico=servico
            ).exclude(
                categoria__id__in=categorias
            ).delete()

            if len(categorias) == qtd_servicos_estoque_invalido:
                return False, erro_msg
            
            return True, erro_msg

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
        servico.status = self.status
        servico.notifica_cliente = self.avisa_cliente
        servico.save()
        return servico.protocolo
    
    def testes(self):
        print(f'Valor da mão de obra: {self.valor_mao_de_obra}')


class EnviaEmail:
    @staticmethod
    def trata_emails(id_servico):
        if settings.DEBUG:
            return
        
        servico_cliente = Servicos.objects.get(id=id_servico)
        
        if servico_cliente.status == 'Em Orçamento' and servico_cliente.notifica_cliente:
            assunto = "AutoSync: Seu orçamento está pronto! Confira os detalhes 💼"

            caminho = r'emails/modelo_em_orcamento.html'
            valida_info_email.delay(id_servico, caminho, assunto)

        elif servico_cliente.status == 'Orçamento Reprovado' and servico_cliente.notifica_cliente:
            assunto = "AutoSync: Orçamento Reprovado - Estamos à disposição para ajustes 💬"

            caminho = r'emails/modelo_orcamento_reprovado.html'
            valida_info_email.delay(id_servico, caminho, assunto)
            
        elif servico_cliente.status == 'Em Andamento' and servico_cliente.notifica_cliente:
            assunto = "AutoSync: Seu serviço está em andamento. Acompanhe o progresso! 🚗"

            caminho = r'emails/modelo_andamento.html'
            valida_info_email.delay(id_servico, caminho, assunto)
        elif servico_cliente.status == 'Finalizado' and servico_cliente.notifica_cliente:
            assunto = 'AutoSync: Tudo pronto! Seu veículo está à sua espera 🚗'

            caminho = r'emails/modelo_finalizado.html'
            valida_info_email.delay(id_servico, caminho, assunto)