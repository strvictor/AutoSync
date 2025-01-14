from estoque.models import Estoque

class ProcessaEstoque: 
    def __init__(self, objeto_categoria_manutencao, quantidade):
        self.erro_msg = None
        self.obj_no_estoque = Estoque.objects.get(nome=objeto_categoria_manutencao)
        self.quantidade = int(quantidade)
       
    def valida_qtd_minima(self):
        quantidade_atual = self.obj_no_estoque.quantidade_em_estoque

        if quantidade_atual < self.quantidade:
            if quantidade_atual == 0:
                self.erro_msg = f'O item "{self.obj_no_estoque.nome}" está em falta no estoque!'
            else:
                self.erro_msg = f'O item "{self.obj_no_estoque.nome}" está com a quantidade em estoque insuficiente. Estoque atual: {quantidade_atual}'
            return False
        
        return True
        
    def retira_qtd_do_estoque(self):
        #TODO - implementar logica, para em caso de edição ele não remover o que ja tinha removido.
        # Exemplo: se cadastrei um item com a quantidade 10 e posteriormente edito ele para a quantidade 5, tenho que voltar 5 pro estoque e não retirar mais 5!
        self.obj_no_estoque.quantidade_em_estoque -= self.quantidade
        self.obj_no_estoque.save()
        return True