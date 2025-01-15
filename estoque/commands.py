from estoque.models import Estoque

class ProcessaEstoque: 
    def __init__(self, objeto_categoria_manutencao, quantidade):
        self.erro_msg = None
        self.obj_no_estoque = Estoque.objects.get(nome=objeto_categoria_manutencao)
        self.quantidade_estoque_atual = self.obj_no_estoque.quantidade_em_estoque
        self.quantidade_repassada = int(quantidade)

    def valida_se_add_ou_acres(self, quantidade_salva):
        if quantidade_salva > self.quantidade_repassada:
            diferenca = quantidade_salva - self.quantidade_repassada
            print(f'Acrescenta {diferenca}')
            self.acrescenta_qtd_do_estoque(diferenca)
        else:
            diferenca = self.quantidade_repassada - quantidade_salva
            print(f'Retira {diferenca}')
            self.retira_qtd_do_estoque(diferenca)

    def valida_qtd_minima(self):
        if self.quantidade_estoque_atual < self.quantidade_repassada:
            if self.quantidade_estoque_atual == 0:
                self.erro_msg = f'O item "{self.obj_no_estoque.nome}" está em falta no estoque!'
            else:
                self.erro_msg = f'O item "{self.obj_no_estoque.nome}" está com a quantidade em estoque insuficiente. Estoque atual: {self.quantidade_estoque_atual}'
            return False
        return True

    def retira_qtd_do_estoque(self, valor):
        self.quantidade_estoque_atual -= valor
        self.obj_no_estoque.quantidade_em_estoque = self.quantidade_estoque_atual
        self.obj_no_estoque.save()
        print(f'Estoque atualizado após retirada: {self.quantidade_estoque_atual}')

    def acrescenta_qtd_do_estoque(self, valor):
        self.quantidade_estoque_atual += valor
        self.obj_no_estoque.quantidade_em_estoque = self.quantidade_estoque_atual
        self.obj_no_estoque.save()
        print(f'Estoque atualizado após acréscimo: {self.quantidade_estoque_atual}')